from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from . import user, seller, items
from .dependencies import *

@asynccontextmanager
async def life_span_session(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=life_span_session)

app.include_router(user.router)
app.include_router(seller.router)
app.include_router(items.router)

@app.post("/register", response_model=UserRead, status_code=201, tags=["users", "sellers", "auth"])
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register new user

    Here we use the `user: UserCreate` as the input, and `UserRead` as the output to avoid leaking password.
    """
    with Session(engine) as session:
        user.password = get_password_hash(user.password)
        user_in_db = User.model_validate(user)
        session.add(user_in_db)
        session.commit()
        session.refresh(user_in_db)
        return user
    
@app.post("/token", tags=["auth"])
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Get token for authentication

    > This can just be copy and paste
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

