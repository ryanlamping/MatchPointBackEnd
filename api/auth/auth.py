# file for api functions regarding authentication

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from crud.crud_user import get_user_by_email, user_sign_up, get_password_hash
from schemas.user import UserCreate, User as Users, UserUpdateEmail as UpdateEmail, UserUpdatePassword as UpdatePassword, Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer  # Added OAuth2PasswordBearer
from db.database import get_db
from crud.crud_user import pwd_context
from core.config import settings
from models.user import User
from schemas.loginRequest import LoginRequest


router = APIRouter()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Log in function
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        return user
    return None

# verify input password matches hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# creating JWT token for authenticated user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# choosing to use form data instead of json here:
@router.post("/token/", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    
    # Handle if user is not in database
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "name": user.name, "nationality": user.nationality, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# find current user through email
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# get current user
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# function to register for the app
@router.post("/signup/", response_model=Users)
def sign_up(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_create.email).first()
    
    # check if email already in database
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_sign_up(db, user_create)

# update user email
@router.post("/update-email")
def update_email(updateEmail: UpdateEmail, db: Session = Depends(get_db)):
    oldEmail = updateEmail.oldEmail
    newEmail = updateEmail.newEmail
    
    user = db.query(User).filter(User.email == oldEmail).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found, current email entered is not associated with an account")
    
    user.email = newEmail
    db.commit()
    db.refresh(user)
    return {"msg": "Email updated successfully"}

# update user password
@router.post("/update-password")
def update_password(updatePassword: UpdatePassword, db: Session = Depends(get_db)):
    email = updatePassword.email
    oldPassword = updatePassword.oldPassword
    newPassword = updatePassword.newPassword
    
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(oldPassword, user.password):
        raise HTTPException(status_code=404, detail="User not found, that email is not associated with an account")
    
    user.password = get_password_hash(newPassword)
    db.commit()
    db.refresh(user)
    return {"msg": "Password updated successfully"}
