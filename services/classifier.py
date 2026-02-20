from pathlib import Path


def load_prompt():
    return Path("prompts/classify.txt").read_text()


async def classify_repository(bundle, llm):
    prompt = load_prompt().format(**bundle)
    return await llm.generate(prompt)