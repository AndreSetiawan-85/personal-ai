"""
Jalankan file ini secara berkala (mis. cron harian):
    python -m app.maintenance
"""

from app.services.consolidation import consolidation_job
from app.services.lifecycle import lifecycle_job


def run_maintenance():
    print("=== Menjalankan consolidation job ===")
    consolidation_job.run()

    print("=== Menjalankan lifecycle job ===")
    lifecycle_job.run()


if __name__ == "__main__":
    run_maintenance()
