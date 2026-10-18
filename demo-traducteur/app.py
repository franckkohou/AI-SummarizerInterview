from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Traducteur IA")

# Model created once, at startup. Temperature 0 = stable, reproducible output.
llm = ChatOllama(model="llama3.2:3b", temperature=0)

TRANSLATION_TEMPLATE = """
You are a professional translator. Translate the text below into {language}.

Rules:
- Keep the meaning and the tone of the original text.
- Output only the translation, with no introduction or explanation.

TEXT: {text}

TRANSLATION:
"""


class TranslationRequest(BaseModel):
    text: str
    language: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/translate")
def translate(data: TranslationRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    prompt = TRANSLATION_TEMPLATE.format(text=data.text, language=data.language)

    try:
        response = llm.invoke(prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ollama error: {exc}")
    translation = response.content.strip()

    if not translation:
        raise HTTPException(status_code=502, detail="The model returned an empty translation")

    return {"translation": translation}


# Keep the frontend mount after the API routes.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    print("Open http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
