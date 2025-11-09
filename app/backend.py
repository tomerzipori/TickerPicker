import glob
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", # when you run Streamlit locally
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=False,
)

logs = glob.glob("logs/*.txt")

@app.get("/log/{date}")
def print_txt(date: str):
    log = f"logs/log-{date}.txt"
    with open(log, 'r') as file:
        content = file.read()
    return PlainTextResponse(content)