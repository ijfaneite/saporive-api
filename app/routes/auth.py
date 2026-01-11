import pytz
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from prisma import Prisma
from passlib.context import CryptContext

from app import schemas


router = APIRouter()

# Load environment variables
load_dotenv()

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get a Prisma client instance
async def get_prisma_client():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username(db: Prisma, username: str):
    return await db.user.find_unique(where={"username": username})

async def authenticate_user(db: Prisma, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashedPassword):
        return None
    return user

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Prisma = Depends(get_prisma_client)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Prisma = Depends(get_prisma_client)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Prisma = Depends(get_prisma_client)):
    db_user = await db.user.find_unique(where={"username": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data.pop("password") # Remove password from the dictionary
    new_user = await db.user.create(
        data={
            **user_data,
            "hashedPassword": hashed_password,
        }
    )

    # Convert UTC timestamps to Caracas timezone
    caracas_tz = pytz.timezone("America/Caracas")
    new_user.createdAt = new_user.createdAt.astimezone(caracas_tz)
    new_user.updatedAt = new_user.updatedAt.astimezone(caracas_tz)
    
    return new_user