from app.services.ollama import ollama_service
from app.services.memory import memory_service
from app.services.memory_parser import memory_parser
from app.services.memory_prompt import MEMORY_EXTRACTION_PROMPT

class MemoryExtractor:

    def extract(self, message):

        if not message or not message.strip():
            return []

        prompt = (
            MEMORY_EXTRACTION_PROMPT
            + "\n"
            + message.strip()
        )

        try:
            response = ollama_service.generate_response(
                prompt
            )

            print("===== RAW MEMORY RESPONSE =====")
            print(response)
            print("===============================")
            
            memories = memory_parser.parse(
                response
            )

        except Exception as e:
            print(
                "Memory extraction error:",
                e
            )
            return []

        saved = []

        for item in memories:

            if not isinstance(item, dict):
                continue

            content = item.get(
                "content"
            )

            tags = item.get(
                "tags",
                []
            )

            importance = item.get(
                "importance",
                5
            )

            confidence = item.get(
                "confidence",
                0.8
            )

            if not content:
                continue

            try:
                importance = int(
                    importance
                )

            except Exception:
                importance = 5

            importance = max(
                1,
                min(
                    importance,
                    10
                )
            )

            try:
                confidence = float(
                    confidence
                )

            except Exception:
                confidence = 0.8

            confidence = max(
                0.0,
                min(
                    confidence,
                    1.0
                )
            )

            if not isinstance(tags, list):
                tags = []

            memory_service.save_memory(
                content=content,
                tags=tags,
                importance=importance,
                confidence=confidence
            )

            saved.append(
                {
                    "content": content,
                    "tags": tags,
                    "importance": importance,
                    "confidence": confidence
                }
            )

        return saved

memory_extractor = MemoryExtractor()