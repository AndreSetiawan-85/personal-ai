from app.services.memory import memory_service

class MemoryExtractor:
    def extract(self, message: str):
        text = message.lower()

        memories = []

        if "nama saya" in text:
            name = message.lower().split("nama saya", 1)[1].strip()

            memories.append(
                {
                    "memory": f"Nama user adalah {name.title()}",
                    "category": "profile",
                    "importance": 10
                }
            )

        if "saya suka" in text:
            preference = message.lower().split("saya suka", 1)[1].strip()

            memories.append(
                {
                    "memory": f"User suka {preference.title()}",
                    "category": "preference",
                    "importance": 8
                }
            )

        for item in memories:
            memory_service.save_memory(
                memory=item["memory"],
                category=item["category"],
                importance=item["importance"]
            )

        return memories

memory_extractor = MemoryExtractor()