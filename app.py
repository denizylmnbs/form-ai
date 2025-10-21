from fastapi import FastAPI, Request
from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file
app = FastAPI()

import io
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
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def fetch_drive_bytes(url: str) -> bytes:
    """
    Büyük dosyalarda Drive 'confirm' çerezini ister; bunu da ele alıyoruz.
    """
    s = requests.Session()
    r = s.get(url, stream=True)
    # confirm token kontrolü
    for k, v in r.cookies.items():
        if k.startswith('download_warning'):
            # token yakalandı → yeniden iste
            r = s.get(url + f"&confirm={v}", stream=True)
            break
    r.raise_for_status()
    return r.content

def docx_text_from_bytes(docx_bytes: bytes) -> str:
    """
    Basit, hızlı çıkarım: paragraflar + tablolar.
    İstersen Mammoth ile daha 'temiz' metin alabilirsin (bkz. altta).
    """
    file_like = io.BytesIO(docx_bytes)
    doc = Document(file_like)

    chunks = []

    # Paragraflar
    for p in doc.paragraphs:
        if p.text.strip():
            chunks.append(p.text)

    # Tablolar
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if any(cells):
                chunks.append(" | ".join(cells))

    # (İsteğe bağlı) header/footer:
    # for section in doc.sections:
    #     if section.header and section.header.paragraphs:
    #         chunks.append("[HEADER] " + " ".join(p.text for p in section.header.paragraphs if p.text.strip()))
    #     if section.footer and section.footer.paragraphs:
    #         chunks.append("[FOOTER] " + " ".join(p.text for p in section.footer.paragraphs if p.text.strip()))

    text = "\n".join(chunks)
    # Fazla boşlukları sadeleştir
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

def read_docx_text_from_drive_open_link(open_link: str) -> str:
    direct = drive_open_link_to_direct(open_link)
    blob = fetch_drive_bytes(direct)
    return docx_text_from_bytes(blob)


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

    text = read_docx_text_from_drive_open_link(cv)

    # API cevap dönmek zorunda
    return {"status": "ok", "received": text}