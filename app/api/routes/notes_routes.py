from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.note_models import NoteCreate, NoteUpdate
from libs.SupabaseCRUD.SupabaseCRUD import SupabaseCRUD

router = APIRouter(prefix="/notes", tags=["Notes"])
db = SupabaseCRUD()

@router.get("/{note_id}")
def get_note(note_id: str):
    """Gets a note by ID."""
    note = db.get_row_by_id("notes", note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("")
def create_note(note: NoteCreate):
    """Creates a new note."""
    result = db.insert_row("notes", jsonable_encoder(note, exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create note")
    return result

@router.put("/{note_id}")
def update_note(note_id: str, note: NoteUpdate):
    """Updates an existing note."""
    result = db.update_row("notes", jsonable_encoder(note, exclude_unset=True), note_id)
    if not result:
         raise HTTPException(status_code=400, detail="Failed to update note")
    return result

@router.delete("/{note_id}")
def delete_note(note_id: str):
    """Deletes an existing note."""
    success = db.delete_row("notes", note_id)
    if not success:
         raise HTTPException(status_code=400, detail="Failed to delete note")
    return {"message": "Note deleted successfully"}
