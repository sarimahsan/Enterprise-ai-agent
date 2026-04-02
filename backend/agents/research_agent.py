from tavily import TavilyClient
from core.config import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def research_company(company: str, goal: str) -> dict:
    news = client.search(
        query=f"{company} latest news challenges problems 2025",
        max_results=3
    )
    about = client.search(
        query=f"{company} what does it do target market customers",
        max_results=3
    )
    goal_context = client.search(
        query=f"{company} {goal}",
        max_results=2
    )

    def extract(results):
        return "\n\n".join(
            f"Source: {r['url']}\n{r['content']}"
            for r in results["results"]
        )

    return {
        "news": extract(news),
        "about": extract(about),
        "goal_context": extract(goal_context)
    }