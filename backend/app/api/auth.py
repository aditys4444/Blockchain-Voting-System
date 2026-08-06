from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from ..models.models import User, AuditLog
from ..schemas.schemas import UserRegister, UserLogin, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account disabled or not found")
    return user

def require_role(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return current_user
    return role_checker

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, request: Request, db: Session = Depends(get_db)):
    # Check existing email/username
    if db.query(User).filter((User.email == user_data.email) | (User.username == user_data.username)).first():
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pwd,
        role=user_data.role or "voter"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log action
    audit = AuditLog(
        user_id=new_user.id,
        user_email=new_user.email,
        action="USER_REGISTER",
        details=f"Registered with role {new_user.role}",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    return new_user

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == login_data.username_or_email) | (User.username == login_data.username_or_email)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username/email or password")
    
    access_token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Log action
    audit = AuditLog(
        user_id=user.id,
        user_email=user.email,
        action="USER_LOGIN",
        details=f"Successful login for role {user.role}",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
