from fastapi import FastAPI, Request
from dotenv import load_dotenv
from main import ai_eval

# load_dotenv()  # Load environment variables from .env file
app = FastAPI()

import json
from io import BytesIO
import mammoth
import re
import requests
from docx import Document  # pip install python-docx

def drive_open_link_to_direct(url: str) -> str:
    """
    https://drive.google.com/open?id=FILE_ID  →  https://drive.google.com/uc?export=download&id=FILE_ID
    """
    m = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if not m:
        raise ValueError("Geçersiz Drive open?id=... linki")
    file_id = m.group(1)
    return f"https://docs.google.com/document/d/{file_id}/export?format=docx"

def docx_to_text_mammoth(url: str) -> str:
    # 1) DOCX baytlarını belleğe çek
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = BytesIO(resp.content)
    print(data)

    # 2) Mammoth ile raw text çıkar
    result = mammoth.extract_raw_text(data)  # .value = str
    text = result.value or ""

    # 3) Basit temizlik: fazla boşlukları sadeleştir
    # İkiden fazla boş satırı teke indir, sağ/sol boşlukları temizle
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


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
    cv = payload.get("cv")

    cv_content = docx_to_text_mammoth(drive_open_link_to_direct(cv))

    payload = {
        "full_name": full_name,
        "email": email,
        "technologies": technologies,
        "about": about,
        "cv": cv_content
    }

    resp = ai_eval(payload)
    data = json.loads(resp)
    return {
            "score": data["score"],
            "strengths": data["strengths"],
            "risks": data["risks"],
            "justification": data["justification"],
            "recommendation": data["recommendation"]
            }
