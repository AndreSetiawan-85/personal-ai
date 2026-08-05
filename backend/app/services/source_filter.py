TRUSTED_SOURCES = {
    "openai.com": 10,
    "blog.google": 10,
    "deepmind.google": 10,
    "microsoft.com": 9,
    "reuters.com": 9,
    "techcrunch.com": 8,
    "theverge.com": 8,
    "wired.com": 7,
    "technologyreview.com": 7,
}

def rank_sources(results):
    ranked = []

    for item in results:
        url = (
            item.get("source", "")
            .lower()
        )

        score = 0

        for domain, value in TRUSTED_SOURCES.items():
            if domain in url:
                score = value
                break

        item["trust_score"] = score

        ranked.append(item)

    ranked.sort(
        key=lambda x: x["trust_score"],
        reverse=True
    )

    return ranked

def get_best_sources(results, minimum_score=7):
    filtered = []

    for item in results:
        if item.get("trust_score", 0) >= minimum_score:
            filtered.append(item)

    return filtered