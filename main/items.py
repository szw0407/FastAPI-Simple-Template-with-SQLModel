from fastapi import APIRouter, Depends, HTTPException

from .dependencies import *

router = APIRouter(
    prefix="/items",
    tags = ["items"],
    dependencies=[Depends(
        get_current_active_user
    )],
    responses={404: {"description": "Not found"}},
)

WRITER_ROLES = ("admin", "seller")

@router.get("/", response_model=List[Item], tags=["admin"])
async def read_items(skip: int = 0, limit: int = 100, admin = Depends(get_current_active_user)):
    """
    Get all items, used by admin only
    """
    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission to get all items")
    with Session(engine) as session:
        items = session.exec(select(Item).offset(skip).limit(limit)).all()
        return items
    
@router.post("/", response_model=Item)
async def create_item(item: ItemCreate, me = Depends(get_current_active_user)):
    """
    Create new item under current user
    """
    if me.role not in WRITER_ROLES:
        raise HTTPException(status_code=403, detail="You don't have permission to create item")
    with Session(engine) as session:
        item_in_db = Item(**item.model_dump(), owner_id=me.id)
        session.add(item_in_db)
        session.commit()
        session.refresh(item_in_db)
        return item_in_db
    
@router.get("/{id}", response_model=ItemRead)
async def read_item(id: int, me = Depends(get_current_active_user)):
    """
    Get item by id
    """
    with Session(engine) as session:
        statement = select(Item, User).join(User).where(Item.id == id)
        result = session.exec(statement).one()
        return ItemRead(
            title = result[0].title,
            description = result[0].description,
            price = result[0].price,
            owner = result[1],
        )
    
@router.put("/{id}", response_model=ItemRead)
async def update_item(id: int, item: ItemCreate, me = Depends(get_current_active_user)):
    """
    Update item by id
    """
    if me.role not in WRITER_ROLES:
        raise HTTPException(status_code=403, detail="You don't have permission to update item")
    with Session(engine) as session:
        item_in_db = session.get(Item, id)
        if not item_in_db:
            raise HTTPException(status_code=404, detail="Item not found")
        elif item_in_db.owner_id != me.id:
            raise HTTPException(status_code=403, detail="You don't have permission to update item")
        item_data = item.model_dump(exclude_unset=True)
        for key, value in item_data.items():
            setattr(item_in_db, key, value)
        session.add(item_in_db)
        session.commit()
        session.refresh(item_in_db)
        return item_in_db
    
@router.delete("/{id}", response_model=Item)
async def delete_item(id: int, me = Depends(get_current_active_user)):
    """
    Delete item by id
    """
    if me.role not in WRITER_ROLES:
        raise HTTPException(status_code=403, detail="You don't have permission to delete item")
    with Session(engine) as session:
        item_in_db = session.get(Item, id)
        if not item_in_db:
            raise HTTPException(status_code=404, detail="Item not found")
        elif item_in_db.owner_id != me.id and me.role != "admin":
            raise HTTPException(status_code=403, detail="You don't have permission to delete item")
        session.delete(item_in_db)
        session.commit()
        return item_in_db
    
@router.put("/{id}/owner", response_model=Item)
async def update_item_owner(id: int, owner_id: int, admin = Depends(get_current_active_user)):
    """
    Update item owner by id
    """
    if admin.role not in WRITER_ROLES:
        raise HTTPException(status_code=403, detail="You don't have permission to update item owner")
    with Session(engine) as session:
        item_in_db = session.get(Item, id)
        if not item_in_db:
            raise HTTPException(status_code=404, detail="Item not found")
        # above we check if item exists, below we check if user exists
        owner_in_db = session.get(User, owner_id)
        if not owner_in_db or owner_in_db.role != "seller":
            raise HTTPException(status_code=422, detail="Owner invalid")
        if item_in_db.owner_id == owner_id:
            raise HTTPException(status_code=400, detail="Owner not changed")
        if admin.id != item_in_db.owner_id and admin.role != "admin":
            raise HTTPException(status_code=403, detail="You don't have permission to update item owner")
        item_in_db.owner_id = owner_id
        session.add(item_in_db)
        session.commit()
        session.refresh(item_in_db)
        return item_in_db