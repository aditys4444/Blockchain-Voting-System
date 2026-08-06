from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: Optional[str] = "voter"

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Candidate Schemas
class CandidateCreate(BaseModel):
    name: str
    party: Optional[str] = None
    manifesto: Optional[str] = None
    avatar_url: Optional[str] = None

class CandidateResponse(CandidateCreate):
    id: int
    election_id: int
    vote_count: int

    class Config:
        from_attributes = True

# Election Schemas
class ElectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "draft"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class ElectionResponse(ElectionCreate):
    id: int
    created_by: int
    created_at: datetime
    candidates: List[CandidateResponse] = []

    class Config:
        from_attributes = True

# Vote Schemas
class VoteCastRequest(BaseModel):
    election_id: int
    candidate_id: int

class VoteReceiptResponse(BaseModel):
    vote_id: int
    election_id: int
    candidate_id: int
    voter_hash: str
    tx_hash: str
    block_index: int
    receipt_hash: str
    created_at: datetime

# Blockchain Schemas
class BlockSchema(BaseModel):
    index: int
    timestamp: float
    previous_hash: str
    hash: str
    nonce: int
    merkle_root: str
    signature: str
    transactions: List[Any]

class ChainStatusSchema(BaseModel):
    is_valid: bool
    total_blocks: int
    difficulty: int
    pending_transactions_count: int
    message: str

# Audit Log Schema
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    user_email: Optional[str]
    action: str
    details: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# AI Anomaly Schema
class FraudAnalysisResult(BaseModel):
    fraud_risk_score: float  # 0.0 to 100.0
    risk_level: str  # Low, Medium, High, Critical
    flagged_anomalies: List[str]
    details: Dict[str, Any]
