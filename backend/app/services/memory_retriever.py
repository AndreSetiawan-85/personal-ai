from app.services.memory import memory_service
from datetime import datetime


class MemoryRetriever:

    def retrieve(self, query, limit=5):

        memories = memory_service.get_memories(limit=100)

        if not memories:
            return []

        query_lower = query.lower()

        aliases = {
            "proyek": [
                "project",
                "software",
                "ai",
                "aplikasi",
                "membuat",
                "membangun"
            ],
            "kerja": [
                "pekerjaan",
                "project",
                "software",
                "ai"
            ],
            "kebiasaan": [
                "habit",
                "productivity",
                "work",
                "fokus"
            ],
            "saya": [],
            "aku": []
        }

        query_words = set(
            query_lower
            .replace("?", "")
            .replace(",", "")
            .split()
        )

        expanded_words = set(query_words)

        for word in query_words:
            if word in aliases:
                expanded_words.update(
                    aliases[word]
                )

        scored = []

        now = datetime.now()

        for item in memories:

            content = item.get(
                "content",
                ""
            ).lower()

            tags = [
                x.lower()
                for x in item.get("tags", [])
            ]

            relevance = 0

            for word in expanded_words:

                if len(word) <= 2:
                    continue

                if word in content:
                    relevance += 5

                if word in tags:
                    relevance += 3

            if relevance == 0:
                continue

            score = relevance

            score += item.get(
                "importance",
                5
            ) * 0.3

            score += item.get(
                "confidence",
                0.5
            ) * 2

            score += min(
                item.get("access_count", 0),
                10
            ) * 0.5

            try:
                last_access = datetime.fromisoformat(
                    item["last_accessed_at"]
                )

                days = (
                    now - last_access
                ).days

                if days == 0:
                    score += 2

                elif days <= 7:
                    score += 1

            except Exception:
                pass

            scored.append(
                (
                    score,
                    item
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        results = [
            item
            for score, item in scored[:limit]
        ]

        for item in results:
            memory_service.touch_memory(
                item["id"]
            )

        return results


memory_retriever = MemoryRetriever()