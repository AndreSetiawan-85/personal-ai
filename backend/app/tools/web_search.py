from ddgs import DDGS

from app.core.config import settings
from app.services.source_validator import filter_trusted_results
from app.tools.registry import tool


def calculate_trust_score(url: str):
    if not url:
        return 0

    normalized_url = url.lower()

    for domain, score in settings.WEB_SEARCH_TRUSTED_SOURCES.items():
        if domain in normalized_url:
            return score

    return settings.WEB_SEARCH_DEFAULT_TRUST_SCORE


def build_search_query(query: str, category: str = None):
    if not category:
        return query

    category_config = settings.WEB_SEARCH_CATEGORIES.get(category)

    if not category_config:
        return query

    domains = category_config.get("domains", [])
    suffix = category_config.get("suffix", "")

    domain_query = " OR ".join(
        f"site:{domain}"
        for domain in domains
    )

    parts = [query]

    if domain_query:
        parts.append(domain_query)

    if suffix:
        parts.append(suffix)

    return " ".join(parts)


@tool(
    name="web_search",
    description="Searches the web for current information and returns trusted sources.",
)
def web_search(
    query: str,
    category: str = None,
    max_results: int = None,
):
    results = []

    if max_results is None:
        max_results = settings.WEB_SEARCH_DEFAULT_MAX_RESULTS

    search_query = build_search_query(
        query,
        category,
    )

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(
                search_query,
                max_results=max_results,
            )

            for item in search_results:
                source = item.get("href")

                results.append(
                    {
                        "title": item.get("title"),
                        "source": source,
                        "snippet": item.get("body"),
                        "trust_score": calculate_trust_score(source),
                    }
                )

        results.sort(
            key=lambda item: item.get("trust_score", 0),
            reverse=True,
        )

        filtered_results = filter_trusted_results(
            results,
            minimum_score=settings.WEB_SEARCH_MINIMUM_TRUST_SCORE,
        )

        return {
            "query": query,
            "search_query": search_query,
            "category": category,
            "results": filtered_results,
        }

    except Exception as e:
        return {
            "query": query,
            "search_query": search_query,
            "category": category,
            "results": [],
            "error": str(e),
        }