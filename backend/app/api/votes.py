from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Election, Candidate, Vote, User, AuditLog
from ..schemas.schemas import VoteCastRequest, VoteReceiptResponse
from .auth import get_current_user
from ..services.blockchain_service import blockchain_service
try:
    from blockchain.wallet import VoterWallet
    from blockchain.cryptography import CryptoEngine
except ImportError:
    from ...blockchain.wallet import VoterWallet
    from ...blockchain.cryptography import CryptoEngine
from ..websockets.manager import manager

router = APIRouter(prefix="/votes", tags=["Voting"])

@router.post("/cast", response_model=VoteReceiptResponse)
async def cast_vote(
    vote_data: VoteCastRequest,
    request: Request,
    db: Session = Depends(get_db),
    voter: User = Depends(get_current_user)
):
    # 1. Verify election exists & is active
    election = db.query(Election).filter(Election.id == vote_data.election_id).first()
    if not election or election.status != "active":
        raise HTTPException(status_code=400, detail="Election is not active for voting")

    # 2. Verify candidate belongs to election
    candidate = db.query(Candidate).filter(
        Candidate.id == vote_data.candidate_id,
        Candidate.election_id == vote_data.election_id
    ).first()
    if not candidate:
        raise HTTPException(status_code=400, detail="Invalid candidate selected for this election")

    # 3. Check for double voting
    existing_vote = db.query(Vote).filter(
        Vote.user_id == voter.id,
        Vote.election_id == vote_data.election_id
    ).first()
    if existing_vote:
        # Audit suspicious double-voting attempt
        audit = AuditLog(
            user_id=voter.id,
            user_email=voter.email,
            action="VOTE_ATTEMPT_DOUBLE",
            details=f"Blocked duplicate vote attempt for Election #{vote_data.election_id}",
            ip_address=request.client.host if request.client else "127.0.0.1"
        )
        db.add(audit)
        db.commit()
        raise HTTPException(status_code=400, detail="You have already cast a vote in this election. Single vote policy enforced.")

    # 4. Generate voter anonymous hash & ECDSA wallet credentials
    wallet = VoterWallet.create_voter_credentials(voter.id, vote_data.election_id)
    voter_hash = wallet["voter_hash"]
    
    # 5. Encrypt vote payload using AES-256 GCM
    encrypted_vote = encrypt_vote_payload(vote_data.candidate_id)

    # 6. Generate digital signature using voter private key
    sig_payload = f"{vote_data.election_id}:{voter_hash}:{encrypted_vote}"
    digital_signature = CryptoEngine.sign_data(wallet["private_key"], sig_payload)

    # 7. Submit transaction to Blockchain & Mine Block
    tx_hash, block_index = blockchain_service.process_vote_transaction(
        db=db,
        election_id=vote_data.election_id,
        voter_hash=voter_hash,
        encrypted_vote=encrypted_vote,
        signature=digital_signature
    )

    # 8. Increment candidate vote tally
    candidate.vote_count += 1

    # 9. Generate receipt metadata
    receipt_data = VoterWallet.generate_receipt(
        tx_hash=tx_hash,
        block_index=block_index,
        voter_hash=voter_hash,
        election_id=vote_data.election_id
    )

    # 10. Record Vote in DB
    new_vote = Vote(
        user_id=voter.id,
        election_id=vote_data.election_id,
        candidate_id=vote_data.candidate_id,
        voter_hash=voter_hash,
        encrypted_vote=encrypted_vote,
        tx_hash=tx_hash,
        block_index=block_index,
        receipt_hash=receipt_data["receipt_hash"]
    )
    db.add(new_vote)

    # Audit log
    audit = AuditLog(
        user_id=voter.id,
        user_email=voter.email,
        action="VOTE_CAST",
        details=f"Cast vote in Election #{vote_data.election_id}. TxHash: {tx_hash[:16]}...",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_vote)

    # Broadcast real-time websocket update
    await manager.broadcast({
        "type": "NEW_VOTE_CAST",
        "election_id": vote_data.election_id,
        "candidate_id": vote_data.candidate_id,
        "block_index": block_index,
        "tx_hash": tx_hash
    })

    return new_vote

@router.get("/my-receipts", response_model=List[VoteReceiptResponse])
def get_my_vote_receipts(
    db: Session = Depends(get_db),
    voter: User = Depends(get_current_user)
):
    return db.query(Vote).filter(Vote.user_id == voter.id).order_by(Vote.created_at.desc()).all()

@router.get("/verify-receipt/{receipt_hash}")
def verify_receipt(receipt_hash: str, db: Session = Depends(get_db)):
    vote = db.query(Vote).filter(Vote.receipt_hash == receipt_hash).first()
    if not vote:
        return {"verified": False, "message": "Receipt hash not found on system record."}
    
    # Cross check blockchain transaction
    tx_data = blockchain_service.blockchain.search_transaction(vote.tx_hash)
    if not tx_data:
        return {"verified": False, "message": "Transaction record not found in Blockchain ledger."}

    return {
        "verified": True,
        "receipt_hash": vote.receipt_hash,
        "election_id": vote.election_id,
        "voter_hash": vote.voter_hash,
        "tx_hash": vote.tx_hash,
        "block_index": vote.block_index,
        "timestamp": vote.created_at
    }
