from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="AI Text Summarizer Interview")

# TODO 0:
# Initialize the Ollama language model using llama3.2:3b
# and configure the temperature .
llm = ChatOllama(model="llama3.2:3b", temperature=0)

SUMMARY_TEMPLATE = """
You are an expert summarizer. Summarize the text below.

Rules:
- Keep only the key ideas; do not copy sentences from the text.
- The summary must be much shorter than the text: 1 to 2 sentences.
- Write in the same language as the text.
- Output only the summary, with no introduction such as "Here is a summary".

TEXT: {text}

SUMMARY:
"""


class SummaryRequest(BaseModel):
    text: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/summarize")
def summarize(data: SummaryRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # TODO 1: Create a prompt asking the AI to summarize data.text
    prompt = SUMMARY_TEMPLATE.format(text=data.text)

    # TODO 2: Send the prompt to Ollama
    # Extract the generated text from the response
    try:
        response = llm.invoke(prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ollama error: {exc}")
    summary = response.content.strip()

    if not summary:
        raise HTTPException(status_code=502, detail="The model returned an empty summary")

    # TODO 3: Return the summary as JSON
    return {"summary": summary}


# Keep the frontend mount after the API routes.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    print("Open http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
