from datetime import datetime

from app.services.memory import memory_service

DECAY_AFTER_DAYS = 30          # mulai decay kalau tak diakses selama X hari
ARCHIVE_CONFIDENCE_FLOOR = 0.3  # di bawah ini, fact di-archive otomatis
DECAY_STEP = 0.1
ACCESS_PROTECTION_COUNT = 5     # fact yang sering diakses dilindungi dari decay


class LifecycleJob:
    """
    Jalankan berkala (mis. sekali sehari). Fact yang jarang diakses dan
    sudah lama idle akan turun confidence-nya bertahap, lalu di-archive
    (bukan dihapus) kalau melewati ambang.
    """

    def run(self):
        memories = memory_service.get_memories(status="active", limit=5000)
        now = datetime.now()

        archived_count = 0
        decayed_count = 0

        for item in memories:
            if item.get("access_count", 0) >= ACCESS_PROTECTION_COUNT:
                continue

            last_accessed = item.get("last_accessed_at")
            if not last_accessed:
                continue

            try:
                last_access_dt = datetime.fromisoformat(last_accessed)
            except Exception:
                continue

            days_idle = (now - last_access_dt).days

            if days_idle < DECAY_AFTER_DAYS:
                continue

            new_confidence = max(0.0, item.get("confidence", 0.8) - DECAY_STEP)
            memory_service.update_confidence(item["id"], new_confidence)
            decayed_count += 1

            if new_confidence <= ARCHIVE_CONFIDENCE_FLOOR:
                memory_service.archive_memory(item["id"])
                archived_count += 1

        print(f"Lifecycle selesai. {decayed_count} fact di-decay, {archived_count} di-archive.")


lifecycle_job = LifecycleJob()

if __name__ == "__main__":
    lifecycle_job.run()
