from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import (
    register_user,
    authenticate_user
)

from app.security import get_current_user

from app.models.user import User

from app.exceptions import (
    UserAlreadyExistsException,
    PhoneNumberAlreadyExistsException,
    InvalidCredentialsException,
    UsernameAlreadyExistsException
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# REGISTER ENDPOINT
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return register_user(
            db,
            user_data
        )

    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    except PhoneNumberAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already exists."
        )

    except UsernameAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )


# LOGIN ENDPOINT
@router.post(
    "/login",
    response_model=TokenResponse
)

def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    try:
        return authenticate_user(
            db,
            login_data
        )

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials."
        )
    



@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user