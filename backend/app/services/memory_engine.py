from app.services.ollama import ollama_service
from app.services.memory_parser import memory_parser
from app.services.memory_prompt import MEMORY_ENGINE_PROMPT
from app.services.conflict_resolver import conflict_resolver


class MemoryEngine:
    def process(self, user_id, message):
        if not message or not message.strip():
            return {
                "need_memory": False,
                "search_query": "",
            }

        prompt = MEMORY_ENGINE_PROMPT + "\n" + message.strip()

        try:
            response = ollama_service.generate_response(prompt)
            data = memory_parser.parse_object(response)
        except Exception as e:
            print("Memory engine error:", e)
            return {
                "need_memory": False,
                "search_query": "",
            }

        self._save_facts(
            user_id=user_id,
            memories=data.get("memories", []),
        )

        return {
            "need_memory": bool(data.get("need_memory", False)),
            "search_query": data.get("search_query") or message,
        }

    def _save_facts(self, user_id, memories):
        if not isinstance(memories, list):
            return

        for item in memories:
            if not isinstance(item, dict):
                continue

            content = item.get("content")

            if not content:
                continue

            tags = item.get("tags", [])

            if not isinstance(tags, list):
                tags = []

            importance = self._clamp_int(
                item.get("importance", 5),
                1,
                10,
            )

            confidence = self._clamp_float(
                item.get("confidence", 0.8),
                0.0,
                1.0,
            )

            try:
                conflict_resolver.resolve_and_save(
                    user_id=user_id,
                    content=content,
                    tags=tags,
                    importance=importance,
                    confidence=confidence,
                )
            except Exception as e:
                print("Save fact error:", e)

    @staticmethod
    def _clamp_int(value, lo, hi):
        try:
            value = int(value)
        except Exception:
            value = lo

        return max(lo, min(value, hi))

    @staticmethod
    def _clamp_float(value, lo, hi):
        try:
            value = float(value)
        except Exception:
            value = lo

        return max(lo, min(value, hi))


memory_engine = MemoryEngine()