from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from planner_api.schemas.users import UserCreate, UserSignIn
from planner_api.databases.database import engine, Base, get_db
from planner_api import crud
from passlib.context import CryptContext

# Router setup
user_router = APIRouter(tags=["User"])
Base.metadata.create_all(bind=engine)

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@user_router.post("/signup")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email already exists"
        )
    
    # Hash the password before saving
    user.password = hash_password(user.password)
    db_user = crud.create_user(db, user)
    return {"message": "User created successfully", "user_id": db_user.id}

@user_router.post("/signin")
async def signin(user: UserSignIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {"message": "User signed in successfully"}

@user_router.delete("/user")
async def delete_user(email: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, email)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the specified email does not exist"
        )
    return {"message": "User deleted successfully"}
