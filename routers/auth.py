from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User, Build  # ✅ Added Build model for saved builds count
from schemas import UserCreate, UserLogin, UserResponse, TokenResponse
import os

# Secret key and token settings
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")  # Use environment variable for security
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI router setup
router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2 scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ✅ Helper function: Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Helper function: Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Helper function: Create JWT token
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Function to get the current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ✅ Fix: Add `/auth/me` endpoint to return user info
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the current logged-in user's details."""
    return UserResponse(id=current_user.id, username=current_user.username, email=current_user.email)

# ✅ Register a new user
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=str(user_data.email), hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(id=new_user.id, username=new_user.username, email=new_user.email)

# ✅ Login endpoint - Returns JWT token
@router.post("/login", response_model=TokenResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found"
        )

    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ✅ NEW: User Dashboard Route - Returns saved builds count
@router.get("/dashboard")
def get_user_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns user details along with the number of saved builds and latest builds."""

    # Fetch saved builds count
    build_count = db.query(Build).filter(Build.user_id == current_user.id).count()

    # Fetch latest 5 saved builds
    latest_builds = db.query(Build).filter(Build.user_id == current_user.id).order_by(Build.id.desc()).limit(5).all()

    return {
        "username": current_user.username,
        "email": current_user.email,
        "user_id": current_user.id,
        "saved_builds": build_count,
        "latest_builds": [{"id": b.id, "name": b.name, "total_price": b.total_price} for b in latest_builds]
    }
