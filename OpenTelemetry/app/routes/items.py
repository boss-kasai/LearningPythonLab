from fastapi import APIRouter

router = APIRouter()


@router.get("/items/{item_id}")
async def read_item(item_id: int) -> dict:
    """アイテム取得 API"""
    return {"item_id": item_id, "description": "Sample Item"}
