from fastapi import APIRouter
from libs.SupabaseCRUD.SupabaseCRUD import SupabaseCRUD

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
db = SupabaseCRUD()

@router.get("/{user_id}")
def get_dashboard_data(user_id: str):
    """Gets all tasks, ideas, notes, and shopitems for a user."""
    return {
        "tasks": db.get_rows_by_field("tasks", "user_id", user_id),
        "ideas": db.get_rows_by_field("ideas", "user_id", user_id),
        "notes": db.get_rows_by_field("notes", "user_id", user_id),
        "shopitems": db.get_rows_by_field("shopitems", "user_id", user_id)
    }
