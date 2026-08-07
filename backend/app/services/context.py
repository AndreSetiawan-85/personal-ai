from app.services.memory_retriever import memory_retriever

class ContextService:
    def build_context(self, query):
        memories = memory_retriever.retrieve(query, limit=5)

        if not memories:
            return ""

        query_lower = query.lower()

        context = "Memory user:\n"

        for item in memories:
            content = item.get("content", "").lower()
            tags = [tag.lower() for tag in item.get("tags", [])]

            if (
                "proyek" in query_lower
                or "project" in query_lower
                or "kerja" in query_lower
                or "pekerjaan" in query_lower
            ):
                if "project" in tags or "ai" in tags or "software" in tags:
                    context += f"- {item['content']}\n"

            elif (
                "kebiasaan" in query_lower
                or "habit" in query_lower
                or "fokus" in query_lower
            ):
                if "habit" in tags or "productivity" in tags or "work" in tags:
                    context += f"- {item['content']}\n"

            else:
                context += f"- {item['content']}\n"

        if context == "Memory user:\n":
            return ""

        print("=== FINAL CONTEXT ===")
        print(context)

        return context

context_service = ContextService()