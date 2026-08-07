from app.services.memory_retriever import memory_retriever


class ContextService:

    def build_context(self, query):

        memories = memory_retriever.retrieve(
            query,
            limit=5
        )

        if not memories:
            return ""

        context = "Memory user:\n"

        for item in memories:
            context += f"- {item['content']}\n"

        return context


context_service = ContextService()