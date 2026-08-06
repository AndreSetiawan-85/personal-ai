from app.services.memory import memory_service


class MemoryExtractor:

    def extract(self, message: str):

        text = message.strip()

        lower = text.lower()

        if lower.startswith("nama saya"):

            name = (
                text[len("nama saya"):]
                .strip()
            )

            if name:

                memory_service.save_memory(
                    "name",
                    name
                )

                return {
                    "key": "name",
                    "value": name
                }

        if lower.startswith("saya suka"):

            preference = (
                text[len("saya suka"):]
                .strip()
            )

            if preference:

                memory_service.save_memory(
                    "preference",
                    preference
                )

                return {
                    "key": "preference",
                    "value": preference
                }

        if lower.startswith("saya bekerja sebagai"):

            job = (
                text[len("saya bekerja sebagai"):]
                .strip()
            )

            if job:

                memory_service.save_memory(
                    "job",
                    job
                )

                return {
                    "key": "job",
                    "value": job
                }

        return None


memory_extractor = MemoryExtractor()