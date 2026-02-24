from fastapi import FastAPI
from pydantic import BaseModel
from services.github_service import fetch_repository_bundle
from services.summarizer import summarize_repository
from utils import logger, SummarizeError, SummarizeSuccess
from config import LLM_PROVIDER
from services.llm.openai_provider import OpenAIProvider
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from requests import Request
import json
import re
from typing import Union

if LLM_PROVIDER == "openai":
    llm = OpenAIProvider()
else:
    raise Exception(f"Currently the only supported LLM is openai, while {LLM_PROVIDER} was requested")

class SummarizeRequest(BaseModel):
    github_url: HttpUrl

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Invalid request format"
        },
    )

@app.post("/summarize", response_model=Union[SummarizeSuccess, SummarizeError])
async def summarize(request: SummarizeRequest):

    try:
        repo_url = str(request.github_url)

        bundle = await fetch_repository_bundle(repo_url)

        logger.info(f"bundle keys: {bundle.keys()}")

        result = await summarize_repository(bundle=bundle, llm=llm)

        logger.info(type(result))
        logger.info(f"result: {result} ### End")

        raw_output = result
        try:
            cleaned = re.sub(r"```json|```", "", result).strip()
            result = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.info(f"parsing error: {e}")
            return SummarizeError(message=f"LLM returned invalid JSON: {e}\nRaw output:\n{raw_output}")

        logger.info("Good Results")
        return SummarizeSuccess(**result)
    
    except Exception as e:
        logger.info("Results Failed")
        return SummarizeError(message=str(e))
