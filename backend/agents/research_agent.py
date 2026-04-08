from tavily import TavilyClient
from core.config import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def research_company(company: str, goal: str) -> dict:
    try:
        news = client.search(
            query=f"{company} latest news challenges problems 2025",
            max_results=3
        )
    except Exception as e:
        print(f"⚠️ Tavily search failed for news: {e}")
        news = {"results": []}
    
    try:
        about = client.search(
            query=f"{company} what does it do target market customers",
            max_results=3
        )
    except Exception as e:
        print(f"⚠️ Tavily search failed for about: {e}")
        about = {"results": []}
    
    try:
        goal_context = client.search(
            query=f"{company} {goal}",
            max_results=2
        )
    except Exception as e:
        print(f"⚠️ Tavily search failed for goal context: {e}")
        goal_context = {"results": []}

    def extract(results):
        if not results.get("results"):
            return f"📊 {company} market research data (API unavailable - using contextual analysis)"
        return "\n\n".join(
            f"Source: {r['url']}\n{r['content']}"
            for r in results["results"]
        )

    return {
        "news": extract(news),
        "about": extract(about),
        "goal_context": extract(goal_context)
    }