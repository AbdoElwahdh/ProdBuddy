from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.task_models import TaskCreate, TaskUpdate
from libs.SupabaseCRUD.SupabaseCRUD import SupabaseCRUD

router = APIRouter(prefix="/tasks", tags=["Tasks"])
db = SupabaseCRUD()



# CRUD
@router.get("/{task_id}")
def get_task(task_id: str):
    """Gets a task by ID."""
    task = db.get_row_by_id("tasks", task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("")
def create_task(task: TaskCreate):
    """Creates a new task."""
    result = db.insert_row("tasks", jsonable_encoder(task, exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return result


@router.put("/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    """Updates an existing task."""
    result = db.update_row("tasks", jsonable_encoder(task, exclude_unset=True), task_id)
    if not result:
         raise HTTPException(status_code=400, detail="Failed to update task")
    return result


@router.delete("/{task_id}")
def delete_task(task_id: str):
    """Deletes an existing task."""
    success = db.delete_row("tasks", task_id)
    if not success:
         raise HTTPException(status_code=400, detail="Failed to delete task")
    return {"message": "Task deleted successfully"}
