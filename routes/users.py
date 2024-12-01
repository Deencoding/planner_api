from fastapi import APIRouter, HTTPException, status
from planner_api.models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])
users = {}

@user_router.post("/signup")
async def create_user(data: User) -> dict:
    # Check if the user already exists in the users dictionary
    if data.email in users:  
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email already exists" 
        )
    users[data.email] = data  # Store the user using their email as the key
    return {
        "message": "User successfully registered"
    }

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    if user.email not in users:  # Check if the user exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    # Check if the password matches
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Wrong credentials passed" 
        )
    return {
        "message": "User signed in successfully"  
    }
