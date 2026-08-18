from app.services.embedding import embedding_service
from app.services.memory import memory_service


class MemoryRetriever:

    def retrieve(self, user_id, query, limit=5):
        if not query or not query.strip():
            return []

        query_embedding = embedding_service.embed(query)

        if not query_embedding:
            return []

        memories = memory_service.get_all_active_with_embeddings(
            user_id=user_id,
        )

        if not memories:
            return []

        scored_memories = []

        for memory in memories:
            embedding = memory.get("embedding")

            if not embedding:
                continue

            score = embedding_service.cosine_similarity(
                query_embedding,
                embedding,
            )

            scored_memories.append(
                (score, memory)
            )

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        results = []

        for score, memory in scored_memories[:limit]:
            memory["similarity"] = score
            results.append(memory)

            try:
                memory_service.touch_memory(
                    memory_id=memory["id"],
                    user_id=user_id,
                )
            except Exception as e:
                print("Memory access update error:", e)

        return results


memory_retriever = MemoryRetriever()