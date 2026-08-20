import threading

from app.database import SessionLocal
from app.services.task_engine import task_engine


class TaskScheduler:
    def __init__(self, interval_seconds: int = 5):
        self.interval_seconds = interval_seconds
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            name="task-scheduler",
            daemon=True,
        )

        self._thread.start()

        print(
            f"[TASK SCHEDULER] Started. "
            f"Interval: {self.interval_seconds}s"
        )

    def stop(self) -> None:
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=10)

        self._thread = None

        print("[TASK SCHEDULER] Stopped.")

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._execute_due_tasks()
            except Exception as exc:
                print(
                    f"[TASK SCHEDULER] Unexpected error: {exc}"
                )

            self._stop_event.wait(
                self.interval_seconds
            )

    def _execute_due_tasks(self) -> None:
        db = SessionLocal()

        try:
            results = task_engine.execute_due_tasks(db)

            if results:
                for result in results:
                    print(
                        f"[TASK SCHEDULER] Executed: {result}"
                    )

        except Exception as exc:
            db.rollback()

            print(
                f"[TASK SCHEDULER] Error: {exc}"
            )

        finally:
            db.close()


task_scheduler = TaskScheduler()