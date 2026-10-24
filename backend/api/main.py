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

pipeline = Pipeline(llm=LLM())


class Query(BaseModel):
    text: str


def is_local_question(text: str) -> bool:
    lower = text.lower()
    local_keywords = [
        "this code",
        "this file",
        "this repository",
        "this module",
        "this api",
        "this function",
        "error",
        "design",
        "implementation",
        "code",
        "class",
        "import",
        "function",
        "architecture",
        "project",
        "bug",
        "fix",
        "refactor",
        "backend",
        "frontend",
        "database",
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "rust",
    ]
    return any(keyword in lower for keyword in local_keywords)


@app.post("/ask")
def ask(query: Query):
    text = query.text.strip()

    if is_local_question(text):
        raw = pipeline.run(text) or {}
        if not isinstance(raw, dict):
            raw = {}

        sections = raw.get("sections", [])
        if not isinstance(sections, list):
            sections = []

        return {
            "mode": "local",
            "title": "ローカル知識ベースの回答",
            "sections": sections
        }

    # 外部検索はユーザーに見せない
    # ここでは内部補助情報を与えて、質問をより確実に処理する
    enriched = pipeline.run(
        f"""
        ユーザーの質問:
        {text}

        補助情報:
        公式ドキュメントと公開情報を補助として確認し、
        最新仕様や一般的な実装方法に沿って回答する。
        """
    ) or {}

    if not isinstance(enriched, dict):
        enriched = {}

    sections = enriched.get("sections", [])
    if not isinstance(sections, list):
        sections = []

    return {
        "mode": "external",
        "title": "内部検索付き回答",
        "sections": sections
    }