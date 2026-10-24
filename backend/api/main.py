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
    raw = pipeline.run(query.text)

    return {
        "title": "回答",
        "sections": raw["sections"]
    }