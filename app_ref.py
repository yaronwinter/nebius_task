from fastapi import FastAPI
from pydantic import BaseModel
from config import LLM_PROVIDER
from observability import REQUEST_COUNT, logger

from services.github_service import fetch_repository_bundle
from services.repo_analyzer import detect_frameworks
from services.classifier import classify_repository
from services.summarizer import summarize_repository
from services.vector_store import VectorStore

from services.llm.openai_provider import OpenAIProvider
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

class SummarizeRequest(BaseModel):
    github_url: str

vector_store = VectorStore()


if LLM_PROVIDER == "openai":
    llm = OpenAIProvider()
else:
    raise Exception(f"Currently the only supported LLM is openai, while {LLM_PROVIDER} was requested")

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    repo_url = request.github_url
    
    # your existing logic
    bundle = await fetch_repository_bundle(repo_url)
    frameworks = detect_frameworks(bundle)
    classification = await classify_repository(
        {**bundle, "frameworks": frameworks}, llm
    )

    return classification
'''
@app.get("/summarize")
async def summarize(repo_url: str, lang: str = "en"):
    REQUEST_COUNT.inc()

    bundle = await fetch_repository_bundle(repo_url)
    frameworks = detect_frameworks(bundle["files"], bundle["readme"])

    classification = await classify_repository(
        {**bundle, "frameworks": frameworks}, llm
    )

    summary = await summarize_repository(
        bundle, frameworks, llm
    )

    embedding = await llm.embed(summary)
    vector_store.add(embedding, {
        "repo": repo_url,
        "summary": summary
    })

    result = {
        "frameworks": frameworks,
        "classification": classification,
        "summary": summary
    }

    await cache.set(cache_key, result)
    logger.info("repo_summarized", repo=repo_url)
    return result
'''

@app.get("/search")
async def search(query: str):
    emb = await llm.embed(query)
    return vector_store.search(emb)

# Mount static directory
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.get("/")
async def root():
    return FileResponse(Path("ui/index.html"))
