from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models.models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class GetUserResponse(BaseModel):
    id: int
    username: str
    email: str


@router.get("/")
async def get_users(db: Session = Depends(get_db)) -> list[GetUserResponse]:
    users = db.query(User).all()
    return [GetUserResponse(id=user.id, username=user.username, email=user.email) for user in users]

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)) -> GetUserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserResponse(id=user.id, username=user.username, email=user.email)

class CreateUserRequest(BaseModel):
    username: str
    email: str

class CreateUserResponse(BaseModel):
    id: int

@router.post("/")
async def create_user(body: CreateUserRequest, db: Session = Depends(get_db)) -> CreateUserResponse:
    user = User(username=body.username, email=body.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return CreateUserResponse(id=user.id)

class DeleteUserResponse(BaseModel):
    message: str

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> DeleteUserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return DeleteUserResponse(message="User deleted successfully")