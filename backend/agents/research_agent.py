from tavily import TavilyClient
from core.config import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def research(goal: str) -> str:
    results = client.search(query=goal, max_results=3)
    combined = "\n\n".join(
        f"Source: {r['url']}\n{r['content']}"
        for r in results["results"]
    )
    return combined