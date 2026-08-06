from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import csv
import io
from ..core.database import get_db
from ..models.models import User, Election, Vote, AuditLog
from ..schemas.schemas import AuditLogResponse
from ..core.security import get_password_hash
from .auth import require_role
from ..services.blockchain_service import blockchain_service

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.get("/metrics")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin"]))
):
    total_elections = db.query(Election).count()
    active_elections = db.query(Election).filter(Election.status == "active").count()
    total_voters = db.query(User).filter(User.role == "voter").count()
    total_votes = db.query(Vote).count()
    is_valid, _ = blockchain_service.blockchain.is_chain_valid()

    return {
        "total_elections": total_elections,
        "active_elections": active_elections,
        "total_voters": total_voters,
        "total_votes": total_votes,
        "blockchain_status": "Healthy" if is_valid else "Compromised",
        "chain_length": len(blockchain_service.blockchain.chain)
    }

@router.post("/import-voters-csv")
async def bulk_import_voters(
    file: UploadFile = File(...),
    request: Request = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin"]))
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV format")

    contents = await file.read()
    reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    imported_count = 0
    errors = []

    for row in reader:
        email = row.get("email")
        username = row.get("username")
        password = row.get("password") or "VoterPass123!"

        if not email or not username:
            continue

        if db.query(User).filter((User.email == email) | (User.username == username)).first():
            errors.append(f"Skipped {email}: Email or Username already exists.")
            continue

        hashed_pwd = get_password_hash(password)
        new_voter = User(email=email, username=username, hashed_password=hashed_pwd, role="voter")
        db.add(new_voter)
        imported_count += 1

    db.commit()

    # Log action
    audit = AuditLog(
        user_id=admin.id,
        user_email=admin.email,
        action="BULK_VOTER_IMPORT",
        details=f"Bulk imported {imported_count} voters from CSV file '{file.filename}'.",
        ip_address=request.client.host if request and request.client else "127.0.0.1"
    )
    db.add(audit)
    db.commit()

    return {
        "imported_count": imported_count,
        "skipped_errors": errors,
        "message": f"Successfully imported {imported_count} voters."
    }

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin", "observer"]))
):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
