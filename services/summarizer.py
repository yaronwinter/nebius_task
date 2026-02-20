from pathlib import Path


def load_prompt():
    return Path("prompts/summarize.txt").read_text()


async def summarize_repository(bundle, frameworks, llm):
    data = {**bundle, "frameworks": frameworks}
    prompt = load_prompt().format(**data)
    return await llm.generate(prompt)