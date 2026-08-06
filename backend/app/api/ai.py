from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.models import User
from ..schemas.schemas import FraudAnalysisResult
from .auth import require_role
from ..services.ai_fraud_service import ai_fraud_service

router = APIRouter(prefix="/ai", tags=["AI Fraud Detection"])

@router.get("/fraud-analysis/{election_id}", response_model=FraudAnalysisResult)
def get_fraud_analysis(
    election_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["admin", "observer"]))
):
    return ai_fraud_service.analyze_voting_health(db, election_id)
