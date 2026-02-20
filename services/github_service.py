import httpx
from urllib.parse import urlparse

GITHUB_API = "https://api.github.com"


def parse_repo(url):
    path = urlparse(url).path.strip("/")
    return path.split("/")[:2]


async def fetch_repository_bundle(repo_url):
    owner, repo = parse_repo(repo_url)

    async with httpx.AsyncClient() as client:
        meta = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}")
        if meta.status_code != 200:
            raise ValueError("Repository not found")

        readme = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/readme",
            headers={"Accept": "application/vnd.github.raw"}
        )

        languages = await client.get(prometheus-client
            f"{GITHUB_API}/repos/{owner}/{repo}/languages"
        )

        tree = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        )

    return {
            "metadata": meta.json(),
            "readme": readme.text if readme.status_code == 200 else "",
            "languages": list(languages.json().keys()),
            "files": [f["path"] for f in tree.json().get("tree", [])]
        }