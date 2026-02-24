import structlog
from pydantic import BaseModel
from typing import List

class SummarizeSuccess(BaseModel):
    summary: str
    technologies: List[str]
    structure: str

class SummarizeError(BaseModel):
    status: str = "error"
    message: str

logger = structlog.get_logger()
