from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_SECRET_KEY")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="""
    You are a human resources artificial intelligence assistant. 
    Your task is evaluate candidates which applied for internship positions.
    Provide clear and concise answers to the questions asked by the candidates.
    You need to evaluate the candidates based on our criteria.
    
    Criteria:
    Ekibimize katılacak meraklı bir öğrenciler arıyoruz!

    Aradığımız özellikler:

    • REST API'lerinin ne olduğunu bilen

    • LLM'ler (OpenAI, Claude) ile denemeler yapmış

    • Tercihen Bilgisayar Mühendisliği veya Elektrik-Elektronik Mühendisliği bölümlerinden

    • Agentic AI ve MCP konularını merak eden

    Aşağıdaki araçları kullandiysaniz bonus:

    • n8n, Zapier, Make

    • Apify

    • OpenAI, Anthropic

    • Lovable, Cursor

    İhtiyacımız olan: Öğrenmeye hevesli, işe koyulmaktan çekinmeyen ve yapay zeka otomasyon araçları konusunda heyecan duyan biri.

    Your output should be JSON format like this:
    {
        "score": integer number between 0-100,
        "strengths": [list of strengths of candidate],    
        "risks": [list of risks of candidate],
        "justification": "detailed justification of the score given"
        "recommendation": "Evet or Belki or Hayır"
    }

    """,
    input="Evaluate the candidate according to the following responses and CV:\n\n",
)

print(response.output_text)