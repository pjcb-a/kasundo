from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse

from app.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.exceptions import (
    UserAlreadyExistsException,
    PhoneNumberAlreadyExistsException,
    InvalidCredentialsException,
    UsernameAlreadyExistsException
)


def get_user_by_username(
    db: Session,
    username: str
):

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )



def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )



def get_user_by_phone(
    db: Session,
    phone_number: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.phone_number == phone_number)
        .first()
    )



def get_user_by_login(
    db: Session,
    login: str
) -> User | None:
    
    if "@" in login:
        return get_user_by_email(
            db, login
        )

    if login.isdigit():
        return get_user_by_phone(
            db, login
        )

    return get_user_by_username(
        db, login
    )



def register_user(
    db: Session, 
    user_data: UserCreate
) -> User:

    existing_email = get_user_by_email(
    db,
    user_data.email
    )

    if existing_email:
        raise UserAlreadyExistsException()


    existing_phone = get_user_by_phone(
        db, 
        user_data.phone_number
    )

    if existing_phone:
        raise PhoneNumberAlreadyExistsException()


    existing_username = get_user_by_username(
        db,
        user_data.username
    )

    if existing_username:
        raise UsernameAlreadyExistsException()



    hashed_password = hash_password(
        user_data.password
    )


    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password_hash=hashed_password
    )


    db.add(user)
    db.commit()
    db.refresh(user)


    return user



def authenticate_user(
    db: Session,
    login_data: LoginRequest
) -> TokenResponse:

    user = get_user_by_login(
        db, 
        login_data.login
    )

    if not user:
        raise InvalidCredentialsException()

    is_valid = verify_password(
        login_data.password,
        user.password_hash
    )

    if not is_valid:
        raise InvalidCredentialsException()

    user.last_login = datetime.now(
        timezone.utc
    )

    db.commit()


    access_token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )