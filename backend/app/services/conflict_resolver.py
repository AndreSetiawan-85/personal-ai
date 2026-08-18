from app.services.embedding import embedding_service
from app.services.ollama import ollama_service
from app.services.memory_parser import memory_parser
from app.services.memory_prompt import CONFLICT_JUDGE_PROMPT
from app.services.memory import memory_service


SIMILARITY_THRESHOLD = 0.55


class ConflictResolver:

    def resolve_and_save(
        self,
        user_id,
        content,
        tags,
        importance,
        confidence,
    ):
        embedding = embedding_service.embed(content)

        candidate = self._find_most_similar(
            user_id=user_id,
            embedding=embedding,
        )

        if candidate:
            relation = self._judge(
                candidate["content"],
                content,
            )

            if relation == "duplicate":
                memory_service.touch_memory(
                    memory_id=candidate["id"],
                    user_id=user_id,
                )
                return None

            if relation == "update":
                new_id = memory_service.save_memory(
                    user_id=user_id,
                    content=content,
                    embedding=embedding,
                    tags=tags,
                    importance=importance,
                    confidence=confidence,
                )

                if new_id:
                    memory_service.supersede_memory(
                        old_id=candidate["id"],
                        new_id=new_id,
                        user_id=user_id,
                    )

                return new_id

        return memory_service.save_memory(
            user_id=user_id,
            content=content,
            embedding=embedding,
            tags=tags,
            importance=importance,
            confidence=confidence,
        )

    def _find_most_similar(self, user_id, embedding):
        if not embedding:
            return None

        existing = memory_service.get_all_active_with_embeddings(
            user_id=user_id,
        )

        best_score = 0.0
        best_item = None

        for item in existing:
            score = embedding_service.cosine_similarity(
                embedding,
                item["embedding"],
            )

            if score > best_score:
                best_score = score
                best_item = item

        if best_item and best_score >= SIMILARITY_THRESHOLD:
            return best_item

        return None

    def _judge(self, old_fact, new_fact):
        prompt = (
            CONFLICT_JUDGE_PROMPT
            .replace("{old_fact}", old_fact)
            .replace("{new_fact}", new_fact)
        )

        try:
            response = ollama_service.generate_response(prompt)
            data = memory_parser.parse_object(response)
            relation = data.get("relation", "unrelated")

            if relation not in (
                "duplicate",
                "update",
                "unrelated",
            ):
                relation = "unrelated"

            return relation

        except Exception as e:
            print("Conflict judge error:", e)
            return "unrelated"


conflict_resolver = ConflictResolver()