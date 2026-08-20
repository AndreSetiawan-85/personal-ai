from datetime import datetime

from sqlalchemy.orm import Session

from app.models.task import Task
from app.services.task_engine import task_engine


class TaskService:
    def create_task(
        self,
        db: Session,
        user_id: int,
        name: str,
        action: str,
        arguments: dict,
        description: str | None = None,
        schedule: str | None = None,
        next_run_at: datetime | None = None,
        max_retries: int = 0,
        retry_delay: int = 60,
    ) -> Task:
        task = Task(
            user_id=user_id,
            name=name,
            description=description,
            action=action,
            arguments=arguments,
            schedule=schedule,
            status="active",
            next_run_at=next_run_at,
            max_retries=max_retries,
            retry_count=0,
            retry_delay=retry_delay,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    def get_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
    ) -> Task | None:
        return (
            db.query(Task)
            .filter(
                Task.id == task_id,
                Task.user_id == user_id,
            )
            .first()
        )

    def list_tasks(
        self,
        db: Session,
        user_id: int,
        status: str | None = None,
    ) -> list[Task]:
        query = (
            db.query(Task)
            .filter(
                Task.user_id == user_id,
            )
        )

        if status is not None:
            query = query.filter(
                Task.status == status,
            )

        return (
            query
            .order_by(Task.created_at.desc())
            .all()
        )

    def update_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
        **updates,
    ) -> Task | None:
        task = self.get_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
        )

        if task is None:
            return None

        allowed_fields = {
            "name",
            "description",
            "action",
            "arguments",
            "schedule",
            "status",
            "next_run_at",
            "max_retries",
            "retry_delay",
        }

        for field, value in updates.items():
            if field not in allowed_fields:
                continue

            setattr(
                task,
                field,
                value,
            )

        db.commit()
        db.refresh(task)

        return task

    def delete_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
    ) -> bool:
        task = self.get_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
        )

        if task is None:
            return False

        db.delete(task)
        db.commit()

        return True

    def pause_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
    ) -> Task | None:
        task = self.get_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
        )

        if task is None:
            return None

        task.status = "paused"

        db.commit()
        db.refresh(task)

        return task

    def resume_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
    ) -> Task | None:
        task = self.get_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
        )

        if task is None:
            return None

        task.status = "active"

        db.commit()
        db.refresh(task)

        return task

    def execute_task(
        self,
        db: Session,
        user_id: int,
        task_id: int,
    ) -> dict:
        task = self.get_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
        )

        if task is None:
            return {
                "success": False,
                "error": "Task not found.",
            }

        return task_engine.execute(
            db=db,
            task=task,
        )


task_service = TaskService()