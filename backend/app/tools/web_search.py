from ddgs import DDGS


def web_search(query: str, max_results: int = 5):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=max_results
        )

        for item in search_results:

            results.append(
                {
                    "title": item.get("title"),
                    "source": item.get("href"),
                    "snippet": item.get("body"),
                }
            )


    return {
        "query": query,
        "results": results
    }