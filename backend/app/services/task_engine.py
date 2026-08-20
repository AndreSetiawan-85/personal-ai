from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_execution import TaskExecution
from app.tools.registry import discover_tools


class TaskExecutionEngine:
    def __init__(self):
        self.tools = discover_tools()

    def execute(
        self,
        db: Session,
        task: Task,
    ) -> dict:
        if task.status != "active":
            return {
                "success": False,
                "task_id": task.id,
                "error": f"Task is not active: {task.status}",
            }

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        # ---------------------------------------------------------
        # EXECUTE TOOL
        # ---------------------------------------------------------
        try:
            result = self.tools.execute(
                task.action,
                task.arguments,
            )
        except Exception as exc:
            result = {
                "success": False,
                "error": str(exc),
            }

        success = result.get("success", False)

        # ---------------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------------
        if success:
            task.run_count += 1

            # Reset retry state after successful execution.
            task.retry_count = 0

            # Clear previous error.
            task.last_error = None

            task.last_run_at = now

            # Calculate the next scheduled execution.
            task.next_run_at = self._calculate_next_run(
                task=task,
                now=now,
            )

        # ---------------------------------------------------------
        # FAILURE
        # ---------------------------------------------------------
        else:
            task.run_count += 1
            task.error_count += 1

            task.last_error = result.get(
                "error",
                "Task execution failed.",
            )

            task.last_run_at = now

            # -----------------------------------------------------
            # RETRY AVAILABLE
            # -----------------------------------------------------
            if task.retry_count < task.max_retries:
                task.retry_count += 1

                task.next_run_at = (
                    now
                    + timedelta(
                        seconds=task.retry_delay,
                    )
                )

            # -----------------------------------------------------
            # RETRIES EXHAUSTED
            # -----------------------------------------------------
            else:
                task.next_run_at = None

        # ---------------------------------------------------------
        # SAVE EXECUTION HISTORY
        # ---------------------------------------------------------
        execution = TaskExecution(
            task_id=task.id,
            success=success,
            result=result,
            error=None if success else result.get("error"),
            executed_at=now,
        )

        db.add(execution)

        # Save task + execution history.
        db.commit()
        db.refresh(task)

        # ---------------------------------------------------------
        # RESPONSE
        # ---------------------------------------------------------
        response = {
            "success": success,
            "task_id": task.id,
            "result": result,
            "executed_at": now,
            "next_run_at": task.next_run_at,
            "run_count": task.run_count,
            "error_count": task.error_count,
            "retry_count": task.retry_count,
            "max_retries": task.max_retries,
            "retry_delay": task.retry_delay,
        }

        if not success:
            response["error"] = task.last_error

        return response

    def execute_due_tasks(
        self,
        db: Session,
    ) -> list[dict]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        tasks = (
            db.query(Task)
            .filter(
                Task.status == "active",
                Task.next_run_at.isnot(None),
                Task.next_run_at <= now,
            )
            .order_by(Task.next_run_at.asc())
            .all()
        )

        results = []

        for task in tasks:
            result = self.execute(
                db=db,
                task=task,
            )

            results.append(result)

        return results

    @staticmethod
    def _calculate_next_run(
        task: Task,
        now: datetime,
    ) -> datetime | None:
        schedule = task.schedule

        if schedule is None:
            return None

        schedule = schedule.strip().lower()

        # One-time task.
        if schedule == "once":
            return None

        # Seconds.
        if schedule.endswith("s"):
            seconds = int(schedule[:-1])

            return now + timedelta(
                seconds=seconds,
            )

        # Minutes.
        if schedule.endswith("m"):
            minutes = int(schedule[:-1])

            return now + timedelta(
                minutes=minutes,
            )

        # Hours.
        if schedule.endswith("h"):
            hours = int(schedule[:-1])

            return now + timedelta(
                hours=hours,
            )

        # Days.
        if schedule.endswith("d"):
            days = int(schedule[:-1])

            return now + timedelta(
                days=days,
            )

        raise ValueError(
            f"Unsupported schedule format: {task.schedule}"
        )


task_engine = TaskExecutionEngine()