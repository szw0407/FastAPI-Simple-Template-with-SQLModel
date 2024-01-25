from fastapi import APIRouter, Depends, HTTPException


from ..models import *
from ..dependencies import *

router = APIRouter(
    prefix="/users",
    tags = ["users"],
    dependencies=[Depends(
        get_current_active_user
    )],
    responses={404: {"description": "Not found"}},
)

class UserModify(BaseModel):
    email: str | None = None
    role: str | None = None
    display_name: str | None = None

    
@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_active_user)):
    """
    Get current user
    """
    return current_user

@router.put("/me", response_model=UserRead)
async def update_users_me(user: UserCreate, current_user: UserRead = Depends(get_current_active_user)):
    """
    Update current user
    """
    user_data = user.model_dump(exclude_unset=True)
    if "password" in user_data:
        hashed_password = get_password_hash(user_data["password"])
        user_data["password"] = hashed_password
    if user_data["role"] != current_user.role:
        raise HTTPException(status_code=403, detail="You don't have permission to update role")
    for key, value in user_data.items():
        setattr(current_user, key, value)
    with Session(engine) as session:
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user

@router.get("/{id}", response_model=UserRead, tags=["admin"])
async def read_user(id: int, depend_user: UserRead = Depends(get_current_active_user)):
    """
    Get user by id, only admin or the user itself can get the user
    """
    if depend_user.role != "admin" and depend_user.id != id:
        raise HTTPException(status_code=403, detail="You don't have permission to get this user")
    with Session(engine) as session:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
@router.get("/", tags=["admin"], response_model=List[UserRead])
async def read_users_admin(skip: int = 0, limit: int = 100, admin = Depends(get_current_active_user)):
    """
    Get all users, used by admin only
    """
    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission to get all users")
    with Session(engine) as session:
        users = session.exec(select(User).offset(skip).limit(limit)).all()
        return users

@router.patch("/{id}", response_model=UserCreate, tags=["admin"])
async def update_user(id: int, user: UserModify, depend_user: UserRead = Depends(get_current_active_user)):
    """
    Update user by id, only admin can update user
    """
    if depend_user.role != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission to update this user")
    with Session(engine) as session:
        user_in_db = session.get(User, id)
        if not user_in_db:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        if "password" in user_data:
            hashed_password = get_password_hash(user_data["password"])
            user_data["password"] = hashed_password
        for key, value in user_data.items():
            setattr(user_in_db, key, value)
        session.add(user_in_db)
        session.commit()
        session.refresh(user_in_db)
        return user_in_db
    
@router.delete("/{id}", response_model=UserRead)
async def delete_user(id: int, depend_user: UserRead = Depends(get_current_active_user)):
    """
    Delete user by id
    """
    if depend_user.role != "admin" and depend_user.id != id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this user")
    with Session(engine) as session:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return user
    
    