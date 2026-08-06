from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import bcrypt
from .config import settings
try:
    from blockchain.cryptography import CryptoEngine
except ImportError:
    from ...blockchain.cryptography import CryptoEngine


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8')[:72], hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8')[:72], salt).decode('utf-8')

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        return {}

def encrypt_vote_payload(candidate_id: int) -> str:
    key = settings.VOTE_ENCRYPTION_KEY.encode('utf-8')[:32]
    return CryptoEngine.encrypt_vote(str(candidate_id), key)

def decrypt_vote_payload(encrypted_vote: str) -> str:
    key = settings.VOTE_ENCRYPTION_KEY.encode('utf-8')[:32]
    return CryptoEngine.decrypt_vote(encrypted_vote, key)
