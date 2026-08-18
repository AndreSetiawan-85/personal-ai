from app.services.memory import memory_service
from app.services.embedding import embedding_service
from app.services.ollama import ollama_service
from app.services.memory_parser import memory_parser
from app.services.memory_prompt import CONSOLIDATION_PROMPT

CLUSTER_SIMILARITY_THRESHOLD = 0.80
MIN_CLUSTER_SIZE = 2


class ConsolidationJob:
    """
    Jalankan berkala (mis. sekali sehari via cron / scheduler).
    Cluster fact yang mirip secara embedding, lalu minta LLM merge jadi
    satu fact yang lebih general. Fact lama ditandai superseded, bukan dihapus.
    """

    def run(self):
        memories = memory_service.get_all_active_with_embeddings()

        if len(memories) < MIN_CLUSTER_SIZE:
            print("Consolidation: belum cukup data untuk clustering.")
            return

        clusters = self._cluster(memories)
        merged_count = 0

        for cluster in clusters:
            if len(cluster) < MIN_CLUSTER_SIZE:
                continue

            merged = self._merge(cluster)
            if not merged:
                continue

            new_content = merged.get("content")
            if not new_content:
                continue

            embedding = embedding_service.embed(new_content)

            new_id = memory_service.save_memory(
                content=new_content,
                embedding=embedding,
                tags=merged.get("tags", []),
                importance=merged.get("importance", 5),
                confidence=merged.get("confidence", 0.8)
            )

            if new_id:
                for old_item in cluster:
                    memory_service.supersede_memory(old_item["id"], new_id)
                merged_count += 1

        print(f"Consolidation selesai. {merged_count} cluster digabung.")

    def _cluster(self, memories):
        clusters = []
        used = set()

        for i, item in enumerate(memories):
            if item["id"] in used:
                continue

            cluster = [item]
            used.add(item["id"])

            for other in memories[i + 1:]:
                if other["id"] in used:
                    continue

                sim = embedding_service.cosine_similarity(
                    item["embedding"], other["embedding"]
                )

                if sim >= CLUSTER_SIMILARITY_THRESHOLD:
                    cluster.append(other)
                    used.add(other["id"])

            clusters.append(cluster)

        return clusters

    def _merge(self, cluster):
        facts_text = "\n".join(f"- {c['content']}" for c in cluster)
        prompt = CONSOLIDATION_PROMPT.replace("{facts}", facts_text)

        try:
            response = ollama_service.generate_response(prompt)
            return memory_parser.parse_object(response)
        except Exception as e:
            print("Consolidation merge error:", e)
            return None


consolidation_job = ConsolidationJob()

if __name__ == "__main__":
    consolidation_job.run()
