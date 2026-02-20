import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async def generate(self, prompt):
        msg = await self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text

    async def embed(self, text):
        raise NotImplementedError("Claude embeddings not implemented")