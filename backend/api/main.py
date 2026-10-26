#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.pipelines.pipeline import Pipeline
from backend.llm.llm import LLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = Pipeline(
    llm=LLM(),
    external_api_key=""
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

    # pipeline 実行
    raw = await pipeline.run(text) or {}

    # 非技術質問なら mode = local
    if raw.get("title") == "非技術質問":
        return build_response(raw, "local")

    # pipeline が外部検索を使ったかどうか
    used_external = raw.get("notes") is not None

    mode = "external" if used_external else "local"

    return build_response(raw, mode)
