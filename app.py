from fastapi import FastAPI
from config import LLM_PROVIDER
from memory_cache import MemoryCache
from observability import REQUEST_COUNT, logger

from services.github_service import fetch_repository_bundle
from services.repo_analyzer import detect_frameworks
from services.classifier import classify_repository
from services.summarizer import summarize_repository
from services.translator import translate
from services.vector_store import VectorStore

from services.llm.openai_provider import OpenAIProvider
from services.llm.claude_provider import ClaudeProvider

app = FastAPI()
cache = MemoryCache()
vector_store = VectorStore()


if LLM_PROVIDER == "openai":
    llm = OpenAIProvider()
else:
    llm = ClaudeProvider()

@app.get("/summarize")
async def summarize(repo_url: str, lang: str = "en"):
    REQUEST_COUNT.inc()
    cache_key = f"{repo_url}:{lang}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    bundle = await fetch_repository_bundle(repo_url)
    frameworks = detect_frameworks(bundle["files"], bundle["readme"])

    classification = await classify_repository(
        {**bundle, "frameworks": frameworks}, llm
    )

    summary = await summarize_repository(
        bundle, frameworks, llm
    )

    if lang != "en":
        summary = await translate(summary, lang, llm)

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


@app.get("/search")
async def search(query: str):
    emb = await llm.embed(query)
    return vector_store.search(emb)