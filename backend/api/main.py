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


@app.post("/ask")
def ask(query: Query):
    text = query.text.strip()

    local_keywords = [
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
        "project",
        "architecture",
        "bug",
        "fix",
        "refactor",
        "system design",
        "backend",
        "frontend",
        "database",
        "python",
        "javascript",
        "typescript",
        "java",
        "c#",
        "go",
        "rust",
    ]

    local_only = any(keyword in text.lower() for keyword in local_keywords)

    if local_only:
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

    return {
        "mode": "external",
        "title": "外部情報が必要",
        "sections": [
            {
                "header": "外部情報が必要です",
                "content": "この質問はローカル知識だけでは十分に答えられません。検索が必要です。"
            }
        ]
    }