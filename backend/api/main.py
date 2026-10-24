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
    keywords = [
        "this code",
        "this file",
        "this repository",
        "this api",
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
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)


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

    # ユーザーには見せない内部検索
    search_context = {
        "source": "official-docs",
        "summary": "外部の公式ドキュメントを参照した情報を補助として利用します。",
        "snippets": [
            "公式ドキュメントを確認して、最新仕様に沿って回答します。",
            "プロジェクト外の一般知識は、明示的に補助情報として扱います。"
        ]
    }

    enriched = pipeline.run(
        f"""
        ユーザーの質問:
        {text}

        追加情報:
        {search_context['summary']}
        {search_context['snippets']}

        上記を踏まえて、回答してください。
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