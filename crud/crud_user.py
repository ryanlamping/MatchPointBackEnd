# create, read, update, and delete user operations

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext
from datetime import date


# password hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# function to create user
def user_sign_up(db: Session, user_create: UserCreate):
    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        name=user_create.name,
        email=user_create.email,
        birthday=user_create.birthday,
        nationality=user_create.nationality,
        password=hashed_password,
        role=user_create.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # need to call login/create token function here to generate token and thus bring user to homescreen
    return new_user

# read user with input of email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
