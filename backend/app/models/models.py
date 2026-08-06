from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="voter")  # admin, voter, observer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    votes = relationship("Vote", back_populates="user")


class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="draft")  # draft, scheduled, active, closed
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    candidates = relationship("Candidate", back_populates="election", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="election", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"), nullable=False)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    manifesto = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    vote_count = Column(Integer, default=0)

    election = relationship("Election", back_populates="candidates")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    election_id = Column(Integer, ForeignKey("elections.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    voter_hash = Column(String, nullable=False, index=True)
    encrypted_vote = Column(Text, nullable=False)
    tx_hash = Column(String, unique=True, index=True, nullable=False)
    block_index = Column(Integer, nullable=True)
    receipt_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="votes")
    election = relationship("Election", back_populates="votes")


class BlockModel(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, unique=True, index=True, nullable=False)
    timestamp = Column(Float, nullable=False)
    previous_hash = Column(String, nullable=False)
    hash = Column(String, unique=True, index=True, nullable=False)
    nonce = Column(Integer, nullable=False)
    merkle_root = Column(String, nullable=False)
    signature = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True, nullable=False)
    block_index = Column(Integer, nullable=False)
    election_id = Column(Integer, nullable=False)
    voter_hash = Column(String, nullable=False)
    encrypted_vote = Column(Text, nullable=False)
    timestamp = Column(Float, nullable=False)
    signature = Column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    user_email = Column(String, nullable=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="info")  # info, success, warning, error
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
