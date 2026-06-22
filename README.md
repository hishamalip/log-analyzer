# 🕵️‍♂️ Log Analyzer Agent

A lightweight, AI-powered Site Reliability Engineering (SRE) assistant built with FastAPI and LangChain. This application allows developers and operations teams to upload raw application logs and instantly receive a human-friendly engineering report complete with extracted anomalies, likely root causes, and actionable next steps.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square\&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138.0-green?style=flat-square\&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-1.3.2-orange?style=flat-square)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI%20Compatible-purple?style=flat-square)

---

## ✨ Features

* **Automated Error Extraction:** Scans raw log lines to capture critical exceptions, errors, and system warnings.
* **Root Cause Analysis:** Translates complex stack traces and cryptic error codes into plain English.
* **Pattern Recognition:** Tracks repeated failures or anomalous trends scattered throughout the log history.
* **Actionable Next Steps:** Generates clear troubleshooting and fixing advice for your engineering team.
* **Mac-Style Terminal UI:** Clean, intuitive front-end featuring a responsive dark theme and seamless upload thresholds.

---

## 🧠 Architecture & How It Works

Processing large log files using Large Language Models (LLMs) can easily bottleneck token limits. To solve this, this agent leverages a smart **Map-Reduce** summarization workflow:

```text
              ┌──────────────────────┐
              │ Uploaded Log File    │
              └──────────┬───────────┘
                         │
                         ▼ (Recursive Chunking)
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 [Log Chunk 1]     [Log Chunk 2]     [Log Chunk 3]
       │                 │                 │
       ▼ (Map Step)      ▼ (Map Step)      ▼ (Map Step)
 [Summary 1]       [Summary 2]       [Summary 3]
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼ (Reduce Step - Synthesis)
           ┌───────────────────────────┐
           │ Final SRE Analysis Report │
           └───────────────────────────┘
```

1. **Chunking:** The backend breaks large log content into small, overlapping chunks using LangChain's text splitters.
2. **Map Step:** Every individual chunk is concurrently processed using a targeted prompt to strip noise and isolate unique facts/errors.
3. **Reduce Step:** The individual summaries are consolidated and passed through a final prompt to synthesize the multi-point structural report.

---

## 📂 Project Structure

As bundled inside Archive.zip, the project contains the following file layout:

```text
├── main.py              # FastAPI application server & routing
├── loganalyzer.py       # Core LLM Map-Reduce orchestration logic
├── index.html           # Single-page frontend application
├── static/
│   └── styles.css       # Mac-terminal aesthetic UI stylesheet
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Uvicorn, Python-Multipart
* **LLM Orchestration:** LangChain (OpenAI Integration)
* **Frontend:** HTML5, CSS3 (Modern Flexbox/Grid), Vanilla JavaScript

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* An OpenAI API Key

> 🔑 **Get your API key from:** https://platform.openai.com/api-keys

### 1. Clone & Navigate

```bash
git clone <your-repo-url>
cd log-analyzer-agent
```

### 2. Environment Setup

Create a virtual environment and activate it:

```bash
# Using standard venv
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

Install the core package rules from the provided file layout:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The agent reads configuration parameters directly from environment variables. You can customize the LLM provider, target model, and connection base URL by setting the variables below:

| Variable Name     | Required | Default Value               | Description                                                                 |
| ----------------- | -------- | --------------------------- | --------------------------------------------------------------------------- |
| `OPENAI_API_KEY`  | **Yes**  | *None*                      | Your OpenAI API credential key.                                             |
| `OPENAI_MODEL`    | No       | `gpt-4o`                    | The target LLM model used for the Map-Reduce summary cycle.                 |
| `OPENAI_BASE_URL` | No       | `https://api.openai.com/v1` | Custom gateway address for LocalAI, Ollama, or alternative reverse proxies. |

#### How to export configurations:

```bash
# Mac/Linux
export OPENAI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

### 5. Launch the Server

Run the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

Open your browser and navigate to **`http://127.0.0.1:8000`** to start analyzing your logs!

---

## 💻 Usage

1. **Access the UI:** Open `http://127.0.0.1:8000` in your web browser.
2. **Select Log File:** Click on the dashboard interface file field or drop a `.txt` or `.log` file up to `1MB` in size.
3. **Analyze:** Click the **Analyse Logs 🚀** button.
4. **Read Report:** Watch the real-time processing terminal report display detailed analysis points mapped straight to your terminal screen.

---

## 🔌 API Endpoints

### 📡 Serve Application Interface

* **URL:** `/`
* **Method:** `GET`
* **Description:** Serves the primary web interface.
* **Response:** HTML application shell interface (`index.html`).

### ⚙️ Stream Log Text Engine

* **URL:** `/analyze`

* **Method:** `POST`

* **Description:** Accepts raw logs and executes the Map-Reduce analysis workflow.

* **Content-Type:** `multipart/form-data`

* **Payload Parameters:**

* `file`: Binary application `.log`/`.txt` file context payload.

* **Success Response (200 OK):**

```json
{
  "analysis": "1. Main Errors: ... \n2. Root Cause: ... \n3. Next Steps: ..."
}
```

* **Error Response Example (400 / 500):**

```json
{
  "error": "Log file is empty"
}
```

---

## 🧪 Testing

You can easily test the endpoint manually via programmatic scripts or tools like `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/application.log"
```
