import os
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI


LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s:%(filename)s:%(funcName)s:%(message)s",
    force=True,
)
logger = logging.getLogger(__name__)


### LLM CONFIGURATION ###
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
app_api_key = os.getenv("OPENAI_API_KEY")  # Reads the API key from environment variables
if not app_api_key:
    logger.error("OPENAI_API_KEY is not set in environment variables. Please set it before running the application.")
    raise ValueError("OPENAI_API_KEY is required but not set.")
print(f"Using OpenAI model: {openai_model} at base URL: {base_url}")

# Initialize the Gemini LLM
llm = ChatOpenAI(
    model=openai_model,
    base_url=base_url,
    api_key=app_api_key
)


# =====================================================================
# PROMPT 1: The "Map" Prompt (Processes individual raw log chunks)
# =====================================================================
chunk_summary_prompt = """
You are a site reliability engineer. 
Analyze the following raw application log segment and extract a highly concise summary of any errors, warnings, exceptions, or anomalous behavior. 
Focus only on facts, error codes, and unique events.

Logs:
{log_data}
"""

# =====================================================================
# PROMPT 2: The "Reduce" Prompt (Synthesizes all summaries into the final report)
# =====================================================================
final_analysis_prompt = """
You are a senior site reliability engineer.

Below is a collection of summaries extracted from different segments of a large log file. 
Analyze these consolidated findings and provide a comprehensive engineering report.

1. Identify the main errors or failures.
2. Explain the likely root cause in simple terms.
3. Suggest practical next steps to fix or investigate.
4. Mention any suspicious patterns or repeated issues across the entire log history.

Log Summaries:
{combined_summaries}

Respond in clear paragraphs. Avoid jargon where possible.
"""


def split_logs(log_file_content):
    """
    Split log text into manageable chunks
    """
    logger.info("Starting log splitting...")
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Adjust chunk size as needed based on typical log file sizes and LLM token limits
        chunk_overlap=200
    )

    log_chunks = recursive_splitter.split_text(log_file_content)
    logger.info(f"Log splitting completed. Total log chunks created: {len(log_chunks)}")
    return log_chunks


def analyze_logs(log_text: str):
    """Analyze logs using Map-Reduce with exactly two dedicated prompts"""
    logger.info("Starting log analysis...")
    chunks = split_logs(log_text)
    
    # Base case: If the file is small and fits in one chunk, 
    if len(chunks) == 1:
        logger.info("Single log chunk detected. Skipping map-reduce step.")
        formatted_prompt = final_analysis_prompt.format(combined_summaries=chunks[0])
        return llm.invoke(formatted_prompt).content

    # --- STEP 1: MAP (Uses Prompt 1) ---
    logger.info("Starting map step: summarizing each log chunk...")
    chunk_summaries = []
    for chunk in chunks:
        formatted_chunk_prompt = chunk_summary_prompt.format(log_data=chunk)
        summary = llm.invoke(formatted_chunk_prompt)
        chunk_summaries.append(summary.content)

    # --- STEP 2: REDUCE (Uses Prompt 2) ---
    logger.info("Starting reduce step: synthesizing all summaries...")
    # Combine the concise chunk summaries together
    combined_summary_input = "\n\n--- Next Segment Summary ---\n\n".join(chunk_summaries)
    
    # Generate the final 4-step report
    final_prompt = final_analysis_prompt.format(combined_summaries=combined_summary_input)
    final_report = llm.invoke(final_prompt)
    logger.info("Final combined analysis: %s", final_report.content)
    
    return final_report.content
