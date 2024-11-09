from pydantic import BaseModel, EmailStr
from datetime import date

# outlining the user types for pydantic and sqlalchemy

# User for registering
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    birthday: date
    nationality: str
    role: int

class User(BaseModel):
    userid: int
    name: str
    email: EmailStr
    birthday: date
    nationality: str
    role: int

    class Config:
        from_attributes = True  # tells Pydantic to treat SQLAlchemy models as dicts
        @staticmethod
        def serialize_birthday(birthday: date) -> str:
            return birthday.isoformat()

        json_encoders = {
            date: serialize_birthday
        }

# user to update email
class UserUpdateEmail(BaseModel):
    oldEmail: EmailStr
    newEmail: EmailStr

# user to update password
class UserUpdatePassword(BaseModel):
    email: EmailStr
    oldPassword: str
    newPassword: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None
    name: str | None = None
    nationality: str | None = None
    role: int | None = None
    