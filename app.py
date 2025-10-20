from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/evaluate")
def evaluate_candidate():
    print("Evaluating candidate...")
    return {"message": "Candidate evaluated"}