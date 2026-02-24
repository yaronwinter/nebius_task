from pathlib import Path
from jinja2 import Template

def load_prompt():
    return Path("prompts/classify.txt").read_text()

async def classify_repository(bundle, llm):
    template = Template(load_prompt())
    prompt = template.render(
        metadata=bundle["metadata"],
        readme=bundle["readme"],
        languages=bundle["languages"],
        files=bundle["files"],
    )
    return await llm.generate(prompt)
