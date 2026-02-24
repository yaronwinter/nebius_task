from fastapi import FastAPI
from pydantic import BaseModel
from services.github_service import fetch_repository_bundle
from services.repo_analyzer import detect_frameworks
from services.classifier import classify_repository
from config import LLM_PROVIDER
from observability import logger
from services.llm.openai_provider import OpenAIProvider

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI()

if LLM_PROVIDER == "openai":
    llm = OpenAIProvider()
else:
    raise Exception(f"Currently the only supported LLM is openai, while {LLM_PROVIDER} was requested")

class SummarizeRequest(BaseModel):
    github_url: HttpUrl


class SummarizeResponse(BaseModel):
    summary: str
    technologies: list[str]
    structure: str


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):

    try:
        repo_url = str(request.github_url)

        bundle = await fetch_repository_bundle(repo_url)
        #frameworks = detect_frameworks(bundle["files"], bundle["readme"])

        logger.info(f"bundle keys: {bundle.keys()}")
        #logger.info(f"frameworks: {type(frameworks)}, content: {frameworks}")

        result = await classify_repository(bundle=bundle, llm=llm)
            #{**bundle, "frameworks": frameworks}, llm
        #)

        logger.info(type(result))
        logger.info(result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
