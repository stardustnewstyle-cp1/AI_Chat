# backend/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.pipelines.pipeline import Pipeline
from backend.llm.llm import LLM
from backend.llm.dummy_model_client import DummyModelClient


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ★ ローカルAI
model_client = DummyModelClient()
llm = LLM(model_client=model_client)

# ★ Pipeline に llm を渡す
pipeline = Pipeline(
    llm=llm,
    external_api_key=""   # 外部検索は使わない
)

class Query(BaseModel):
    text: str


def build_response(raw: dict | None, mode: str) -> dict:
    if not isinstance(raw, dict):
        raw = {}

    sections = raw.get("sections", [])
    if not isinstance(sections, list):
        sections = []

    title = raw.get("title") or (
        "ローカル知識ベースの回答" if mode == "local" else "内部検索付き回答"
    )

    return {
        "mode": mode,
        "title": title,
        "intent": raw.get("intent"),
        "reasoning": raw.get("reasoning"),
        "level": raw.get("level"),
        "score": raw.get("score"),
        "sections": sections,
    }


@app.post("/ask")
async def ask(query: Query):
    text = query.text.strip()

    raw = await pipeline.run(text) or {}

    if raw.get("title") == "非技術質問":
        return build_response(raw, "local")

    used_external = raw.get("notes") is not None
    mode = "external" if used_external else "local"

    return build_response(raw, mode)
