from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


class RoleName(str, Enum):  # To define all possible roles in the system
    admin = "admin"
    seller = "seller"
    user = "user"

# Below we define the models for the database
class UserBase(SQLModel):
    email: str = Field(index=True)
    display_name: str
    role : RoleName = Field(default="user")

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # primary key, auto increment
    password: str  # hashed password in database

class UserCreate(UserBase):
    password: str  # plain password from user input

class UserRead(UserBase):
    pass

class SellerInfo(UserBase):
    items : Optional[List["Item"]] = Relationship(back_populates="owner")

class ItemsBase(SQLModel):
    title: str  # item title
    description: Optional[str] = None  # item description
    price: float = Field(ge=0)  # item price, must not be negative

class Item(ItemsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # primary key, auto increment
    owner_id: int = Field(foreign_key="user.id")  # foreign key to user table

class ItemCreate(ItemsBase):
    pass

class ItemRead(ItemsBase):
    owner: UserRead

class TokenData(BaseModel): 
    username: str