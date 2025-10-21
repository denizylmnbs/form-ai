from fastapi import FastAPI
from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/evaluate")
def evaluate_candidate(request):
    payload = request.json()

    full_name = payload.get("full_name")
    email = payload.get("email")
    technologies = payload.get("technologies")
    about = payload.get("about")
    cv = payload.get("cv")
    
    cv_name = cv.get("name")
    cv_link = cv.get("webViewLink")

    print(f"Evaluating candidate: {full_name}, Email: {email}, CV: {cv_name}, Link: {cv_link}, Technologies: {technologies}, About: {about}")