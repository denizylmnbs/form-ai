from fastapi import FastAPI, Request
from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/evaluate")
async def evaluate_candidate(request: Request):
    payload = await request.json()  # <-- await önemli!

    full_name = payload.get("full_name")
    email = payload.get("email")
    technologies = payload.get("technologies")
    about = payload.get("about")
    cv = payload.get("cv") or {}

    cv_name = cv.get("name")
    cv_link = cv.get("webViewLink")

    print(f"Evaluating candidate: {full_name}, Email: {email}, CV: {cv_name}, Link: {cv_link}, Technologies: {technologies}, About: {about}")

    # API cevap dönmek zorunda
    return {"status": "ok", "received": payload}