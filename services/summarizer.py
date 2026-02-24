from pathlib import Path
from jinja2 import Template
import json

def load_prompt():
    return Path("prompts/summarize.txt").read_text()

async def summarize_repository(bundle, llm):
    template = Template(load_prompt())
    prompt = template.render(
        metadata=json.dumps(bundle["metadata"], indent=2),
        readme=bundle["readme"],
        languages=json.dumps(bundle["languages"], indent=2),
        files=json.dumps(bundle["files"], indent=2),
    )

    return await llm.generate(prompt)
