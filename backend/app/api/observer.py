from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..core.database import get_db
from ..models.models import Election, Candidate, Vote, AuditLog
from ..services.blockchain_service import blockchain_service

router = APIRouter(prefix="/observer", tags=["Observer Transparency"])

@router.get("/live-results/{election_id}")
def get_live_election_results(election_id: int, db: Session = Depends(get_db)):
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    candidates = db.query(Candidate).filter(Candidate.election_id == election_id).all()
    total_votes = db.query(Vote).filter(Vote.election_id == election_id).count()

    results = []
    for c in candidates:
        percentage = round((c.vote_count / total_votes * 100), 2) if total_votes > 0 else 0.0
        results.append({
            "candidate_id": c.id,
            "name": c.name,
            "party": c.party,
            "vote_count": c.vote_count,
            "percentage": percentage
        })

    is_valid, _ = blockchain_service.blockchain.is_chain_valid()

    return {
        "election_id": election.id,
        "title": election.title,
        "status": election.status,
        "total_votes": total_votes,
        "candidates": results,
        "blockchain_verified": is_valid
    }
