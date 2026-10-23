#main.py#
from fastapi import FastAPI
from pydantic import BaseModel
from pipelines.pipeline import Pipeline
from llm.llm import LLM

app = FastAPI()
pipeline = Pipeline(llm=LLM())

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask(query: Query):
    return pipeline.run(query.text)
