from datetime import timedelta
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import UserCreate, User, UserLogin
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user_from_cookie,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.database.connection import users_collection

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=User)
async def signup(user_data: UserCreate):
    # Check if username already exists
    if users_collection.find_one({"username": user_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    user_id = ObjectId()
    user_dict = user_data.model_dump(mode="json")
    password = user_dict.pop("password")

    new_user = {
        "_id": user_id,
        "id": str(user_id),
        "password_hash": get_password_hash(password),
        **user_dict
    }

    users_collection.insert_one(new_user)

    return User(
        id=str(user_id),
        username=user_data.username,
        name=user_data.name,
        role=user_data.role
    )


@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    # Set cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_user_from_cookie)):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user_from_cookie)):
    return current_user
