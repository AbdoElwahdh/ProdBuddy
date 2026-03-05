from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.idea_models import IdeaCreate, IdeaUpdate
from libs.SupabaseCRUD.SupabaseCRUD import SupabaseCRUD

router = APIRouter(prefix="/ideas", tags=["Ideas"])
db = SupabaseCRUD()

@router.get("/{idea_id}")
def get_idea(idea_id: str):
    """Gets an idea by ID."""
    idea = db.get_row_by_id("ideas", idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea

@router.post("")
def create_idea(idea: IdeaCreate):
    """Creates a new idea."""
    result = db.insert_row("ideas", jsonable_encoder(idea, exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create idea")
    return result

@router.put("/{idea_id}")
def update_idea(idea_id: str, idea: IdeaUpdate):
    """Updates an existing idea."""
    result = db.update_row("ideas", jsonable_encoder(idea, exclude_unset=True), idea_id)
    if not result:
         raise HTTPException(status_code=400, detail="Failed to update idea")
    return result

@router.delete("/{idea_id}")
def delete_idea(idea_id: str):
    """Deletes an existing idea."""
    success = db.delete_row("ideas", idea_id)
    if not success:
         raise HTTPException(status_code=400, detail="Failed to delete idea")
    return {"message": "Idea deleted successfully"}
