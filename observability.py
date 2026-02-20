import structlog
from prometheus_client import Counter, Histogram

logger = structlog.get_logger()

REQUEST_COUNT = Counter("api_requests_total", "Total API requests")
LLM_LATENCY = Histogram("llm_latency_seconds", "LLM call latency")