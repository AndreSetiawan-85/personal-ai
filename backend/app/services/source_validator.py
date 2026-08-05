from urllib.parse import urlparse

TRUSTED_DOMAINS = {
    "high": [
        "reuters.com",
        "openai.com",
        "blog.google",
        "microsoft.com",
        "github.com",
        "python.org",
        "nature.com",
        "arxiv.org",
    ],
    "medium": [
        "techcrunch.com",
        "wired.com",
        "theverge.com",
        "bbc.com",
        "cnn.com",
        "allrecipes.com",
        "foodnetwork.com",
        "tripadvisor.com",
        "booking.com",
    ],
}

def get_domain(url: str):
    try:
        return (
            urlparse(url)
            .netloc
            .lower()
            .replace("www.", "")
        )
    except Exception:
        return ""

def validate_source(url: str):
    domain = get_domain(url)

    if not domain:
        return {
            "level": "unknown",
            "score": 20
        }

    for source in TRUSTED_DOMAINS["high"]:
        if source in domain:
            return {
                "level": "high",
                "score": 100
            }

    for source in TRUSTED_DOMAINS["medium"]:
        if source in domain:
            return {
                "level": "medium",
                "score": 70
            }

    return {
        "level": "normal",
        "score": 50
    }

def filter_trusted_results(results, minimum_score=50):
    validated = []

    for item in results:
        validation = validate_source(
            item.get("source")
        )

        item.update(
            {
                "source_level": validation["level"],
                "source_score": validation["score"]
            }
        )

        if validation["score"] >= minimum_score:
            validated.append(item)

    return validated