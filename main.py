from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from loganalyzer import analyze_logs


app = FastAPI(title="Log Analyzer Agent")

# ADD THIS LINE: Mounts the "static" folder to the "/static" URL path
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()


@app.post("/analyze")
async def analyse_log_file(file: UploadFile = File()):
    """Analyse uploaded log file"""
    try:
        log_file = await file.read()
        log_file_content = log_file.decode("utf-8", errors="ignore")

        if not log_file_content:
            return JSONResponse(
                status_code=400,
                content={"error": "Log file is empty"}
            )
        
        result = analyze_logs(log_file_content)
        return {"analysis": result}

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Error analysing logs: {str(ex)}"
            }
        )
    
