from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.shopitem_models import ShopItemCreate, ShopItemUpdate
from libs.SupabaseCRUD.SupabaseCRUD import SupabaseCRUD

router = APIRouter(prefix="/shopitems", tags=["ShopItems"])
db = SupabaseCRUD()

@router.get("/{item_id}")
def get_shopitem(item_id: str):
    """Gets a shop item by ID."""
    item = db.get_row_by_id("shopitems", item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return item

@router.post("")
def create_shopitem(item: ShopItemCreate):
    """Creates a new shop item."""
    result = db.insert_row("shopitems", jsonable_encoder(item, exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create shop item")
    return result

@router.put("/{item_id}")
def update_shopitem(item_id: str, item: ShopItemUpdate):
    """Updates an existing shop item."""
    result = db.update_row("shopitems", jsonable_encoder(item, exclude_unset=True), item_id)
    if not result:
         raise HTTPException(status_code=400, detail="Failed to update shop item")
    return result

@router.delete("/{item_id}")
def delete_shopitem(item_id: str):
    """Deletes an existing shop item."""
    success = db.delete_row("shopitems", item_id)
    if not success:
         raise HTTPException(status_code=400, detail="Failed to delete shop item")
    return {"message": "Shop item deleted successfully"}
