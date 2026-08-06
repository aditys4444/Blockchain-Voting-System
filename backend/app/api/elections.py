from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Election, Candidate, User, AuditLog
from ..schemas.schemas import ElectionCreate, ElectionResponse, CandidateCreate, CandidateResponse
from .auth import get_current_user, require_role
from ..websockets.manager import manager

router = APIRouter(prefix="/elections", tags=["Elections"])

@router.get("", response_model=List[ElectionResponse])
def get_all_elections(db: Session = Depends(get_db)):
    return db.query(Election).order_by(Election.created_at.desc()).all()

@router.get("/{election_id}", response_model=ElectionResponse)
def get_election(election_id: int, db: Session = Depends(get_db)):
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    return election

@router.post("", response_model=ElectionResponse)
async def create_election(
    election_data: ElectionCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin"]))
):
    new_election = Election(
        title=election_data.title,
        description=election_data.description,
        status=election_data.status or "draft",
        start_time=election_data.start_time,
        end_time=election_data.end_time,
        created_by=admin.id
    )
    db.add(new_election)
    db.commit()
    db.refresh(new_election)

    # Log action
    audit = AuditLog(
        user_id=admin.id,
        user_email=admin.email,
        action="ELECTION_CREATE",
        details=f"Created election ID #{new_election.id}: '{new_election.title}'",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    await manager.broadcast({"type": "ELECTION_UPDATE", "action": "CREATE", "election_id": new_election.id})
    return new_election

@router.put("/{election_id}/status")
async def update_election_status(
    election_id: int,
    status_val: str,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin"]))
):
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    
    if status_val not in ["draft", "scheduled", "active", "closed"]:
        raise HTTPException(status_code=400, detail="Invalid election status")

    election.status = status_val
    db.commit()

    audit = AuditLog(
        user_id=admin.id,
        user_email=admin.email,
        action="ELECTION_STATUS_CHANGE",
        details=f"Election ID #{election_id} status changed to '{status_val}'",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    await manager.broadcast({"type": "ELECTION_STATUS_CHANGE", "election_id": election_id, "status": status_val})
    return {"message": f"Election status updated to {status_val}"}

@router.post("/{election_id}/candidates", response_model=CandidateResponse)
async def add_candidate(
    election_id: int,
    candidate_data: CandidateCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin"]))
):
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    new_candidate = Candidate(
        election_id=election_id,
        name=candidate_data.name,
        party=candidate_data.party,
        manifesto=candidate_data.manifesto,
        avatar_url=candidate_data.avatar_url,
        vote_count=0
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    audit = AuditLog(
        user_id=admin.id,
        user_email=admin.email,
        action="CANDIDATE_ADD",
        details=f"Added candidate '{new_candidate.name}' to Election #{election_id}",
        ip_address=request.client.host if request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    await manager.broadcast({"type": "CANDIDATE_ADD", "election_id": election_id, "candidate_id": new_candidate.id})
    return new_candidate
