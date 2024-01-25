from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .dependencies import *

router = APIRouter(
    prefix="/sellers",
    tags = ["sellers"],
    dependencies=[Depends(
        get_current_active_user
    )],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=SellerInfo)
async def read_seller(id: int):
    """
    Get seller by id
    """
    with Session(engine) as session:
        user = session.get(User, id)
        if not user or user.role != "seller":
            raise HTTPException(status_code=404, detail="Seller not found")
        items = session.exec(select(Item).where(Item.owner_id == id))
        return SellerInfo(
            email = user.email,
            display_name = user.display_name,
            role = user.role,
            items= [_ for _ in items]
        )
    
@router.get("/", response_model=List[UserRead])
async def read_sellers(skip: int = 0, limit: int = 100):
    """
    Get all sellers
    """
    with Session(engine) as session:
        sellers = session.exec(select(User).where(User.role == "seller").offset(skip).limit(limit)).all()
        return sellers
    
@router.get("/{id}/items", response_model=List[ItemRead])
async def read_seller_items(id: int, skip: int = 0, limit: int = 100):
    """
    Get seller items by id
    """
    with Session(engine) as session:
        seller = session.get(User, id)
        if not seller:
            raise HTTPException(status_code=404, detail="Seller not found")
        items = session.exec(select(Item).where(Item.owner_id == id).offset(skip).limit(limit)).all()
        return items
    
