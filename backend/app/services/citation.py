from datetime import datetime


def format_citations(results):
    citations = []

    checked_time = datetime.now().strftime("%A, %d %B %Y %H:%M")

    for item in results:
        citations.append(
            {
                "title": item.get("title", "Unknown"),
                "source": item.get("source", ""),
                "source_level": item.get("source_level", "normal"),
                "source_score": item.get("source_score", 50),
                "checked_at": checked_time,
            }
        )

    return citations
