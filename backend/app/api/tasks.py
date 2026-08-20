from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task_execution import TaskExecution
from app.services.task import task_service


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class TaskCreateRequest(BaseModel):
    user_id: int
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    action: str
    arguments: dict = Field(
        default_factory=dict,
    )
    description: str | None = None
    schedule: str | None = None
    next_run_at: datetime | None = None

    max_retries: int = Field(
        default=0,
        ge=0,
        le=100,
    )

    retry_delay: int = Field(
        default=60,
        ge=1,
        le=86400,
    )


class TaskUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None
    action: str | None = None
    arguments: dict | None = None
    schedule: str | None = None
    status: str | None = None
    next_run_at: datetime | None = None

    max_retries: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    retry_delay: int | None = Field(
        default=None,
        ge=1,
        le=86400,
    )


# ============================================================
# SERIALIZERS
# ============================================================

def serialize_task(task):
    return {
        "id": task.id,
        "user_id": task.user_id,
        "name": task.name,
        "description": task.description,
        "action": task.action,
        "arguments": task.arguments,
        "schedule": task.schedule,
        "status": task.status,

        "last_run_at": task.last_run_at,
        "next_run_at": task.next_run_at,

        "run_count": task.run_count,
        "error_count": task.error_count,
        "last_error": task.last_error,

        "max_retries": task.max_retries,
        "retry_count": task.retry_count,
        "retry_delay": task.retry_delay,

        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


def serialize_execution(execution):
    return {
        "id": execution.id,
        "task_id": execution.task_id,
        "success": execution.success,
        "result": execution.result,
        "error": execution.error,
        "executed_at": execution.executed_at,
    }


# ============================================================
# CREATE TASK
# ============================================================

@router.post("")
def create_task(
    payload: TaskCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        task = task_service.create_task(
            db=db,
            user_id=payload.user_id,
            name=payload.name,
            action=payload.action,
            arguments=payload.arguments,
            description=payload.description,
            schedule=payload.schedule,
            next_run_at=payload.next_run_at,
            max_retries=payload.max_retries,
            retry_delay=payload.retry_delay,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return serialize_task(task)


# ============================================================
# LIST TASKS
# ============================================================

@router.get("")
def list_tasks(
    user_id: int,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    tasks = task_service.list_tasks(
        db=db,
        user_id=user_id,
        status=status,
    )

    return [
        serialize_task(task)
        for task in tasks
    ]


# ============================================================
# GET TASK
# ============================================================

@router.get("/{task_id}")
def get_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return serialize_task(task)


# ============================================================
# TASK STATUS
# ============================================================

@router.get("/{task_id}/status")
def get_task_status(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return {
        "task_id": task.id,
        "name": task.name,
        "status": task.status,
        "schedule": task.schedule,

        "run_count": task.run_count,
        "error_count": task.error_count,
        "last_error": task.last_error,

        "retry_count": task.retry_count,
        "max_retries": task.max_retries,
        "retry_delay": task.retry_delay,

        "last_run_at": task.last_run_at,
        "next_run_at": task.next_run_at,
    }


# ============================================================
# EXECUTION HISTORY
# ============================================================

@router.get("/{task_id}/executions")
def list_task_executions(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    executions = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.task_id == task_id,
        )
        .order_by(
            TaskExecution.executed_at.desc(),
        )
        .all()
    )

    return [
        serialize_execution(execution)
        for execution in executions
    ]


# ============================================================
# UPDATE TASK
# ============================================================

@router.put("/{task_id}")
def update_task(
    task_id: int,
    user_id: int,
    payload: TaskUpdateRequest,
    db: Session = Depends(get_db),
):
    updates = payload.model_dump(
        exclude_unset=True,
    )

    try:
        task = task_service.update_task(
            db=db,
            user_id=user_id,
            task_id=task_id,
            **updates,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return serialize_task(task)


# ============================================================
# DELETE TASK
# ============================================================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    deleted = task_service.delete_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return {
        "success": True,
        "message": "Task deleted.",
    }


# ============================================================
# PAUSE TASK
# ============================================================

@router.post("/{task_id}/pause")
def pause_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.pause_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return serialize_task(task)


# ============================================================
# RESUME TASK
# ============================================================

@router.post("/{task_id}/resume")
def resume_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.resume_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return serialize_task(task)


# ============================================================
# MANUAL EXECUTION
# ============================================================

@router.post("/{task_id}/execute")
def execute_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    result = task_service.execute_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if not result.get("success"):
        error = result.get(
            "error",
            "Task execution failed.",
        )

        if error == "Task not found.":
            raise HTTPException(
                status_code=404,
                detail=error,
            )

        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return result