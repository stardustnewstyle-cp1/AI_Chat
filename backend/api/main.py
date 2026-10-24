from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.pipelines.pipeline import Pipeline
from backend.pipelines.pipeline_code import CodePipeline
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
code_pipeline = CodePipeline(llm=LLM())

class Query(BaseModel):
    text: str


def should_use_code_mode(text: str) -> bool:
    lower = text.lower()
    keywords = [
        "コード",
        "コード例",
        "実装例",
        "サンプルコード",
        "書いて",
        "例を見せて",
        "api の使い方",
        "関数",
        "class",
    ]
    return any(keyword in lower for keyword in keywords)


@app.post("/ask")
def ask(query: Query):
    text = query.text

    if should_use_code_mode(text):
        result = code_pipeline.run(text, api_info=None)

        code_text = None
        if result.get("llm_output") is not None:
            code_text = result["llm_output"]
        elif result.get("code_output") is not None:
            code_text = result["code_output"]

        if code_text is None:
            code_text = "コード生成用の情報が不足しています。"

        return {
            "mode": "code",
            "title": "コード例",
            "sections": [
                {"header": "コード", "code": code_text}
            ]
        }

    raw = pipeline.run(text)

    return {
        "mode": "answer",
        "title": "回答",
        "sections": raw["sections"]
    }