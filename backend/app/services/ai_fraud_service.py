import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.models import Vote, AuditLog

class AIFraudService:
    """
    AI & Machine Learning Anomaly Detection Module for Voting Security.
    Analyzes vote timing distributions, IP bursts, duplicate attempts, 
    and voting speed metrics to compute a Fraud Risk Score (0 - 100%).
    """
    @staticmethod
    def analyze_voting_health(db: Session, election_id: int) -> Dict[str, Any]:
        votes = db.query(Vote).filter(Vote.election_id == election_id).order_by(Vote.created_at.asc()).all()
        audit_logs = db.query(AuditLog).filter(AuditLog.action.in_(["VOTE_CAST", "VOTE_ATTEMPT_DOUBLE"])).all()

        total_votes = len(votes)
        flagged_anomalies = []
        fraud_risk_score = 0.0

        if total_votes == 0:
            return {
                "fraud_risk_score": 0.0,
                "risk_level": "Low",
                "flagged_anomalies": ["No votes recorded yet."],
                "details": {
                    "total_votes": 0,
                    "rapid_burst_count": 0,
                    "duplicate_ip_count": 0,
                    "double_voting_attempts": 0
                }
            }

        # 1. Detect Double Voting Attempts from Audit Logs
        double_vote_logs = [log for log in audit_logs if log.action == "VOTE_ATTEMPT_DOUBLE"]
        double_voting_attempts = len(double_vote_logs)
        if double_voting_attempts > 0:
            flagged_anomalies.append(f"Detected {double_voting_attempts} blocked double-voting attempts.")
            fraud_risk_score += min(double_voting_attempts * 15.0, 45.0)

        # 2. Velocity Analysis (Rapid Burst Detection: votes within 2 seconds)
        rapid_burst_count = 0
        timestamps = [v.created_at.timestamp() for v in votes]
        for i in range(1, len(timestamps)):
            if timestamps[i] - timestamps[i - 1] < 2.0:
                rapid_burst_count += 1

        if rapid_burst_count > 0:
            burst_ratio = rapid_burst_count / total_votes
            if burst_ratio > 0.2:
                flagged_anomalies.append(f"High velocity anomaly: {rapid_burst_count} votes cast within 2 seconds of each other.")
                fraud_risk_score += min(burst_ratio * 50.0, 35.0)

        # 3. IP Concentration Analysis
        ip_counts: Dict[str, int] = {}
        vote_logs = [log for log in audit_logs if log.action == "VOTE_CAST"]
        for log in vote_logs:
            ip = log.ip_address or "127.0.0.1"
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

        duplicate_ip_count = sum(1 for count in ip_counts.values() if count > 5)
        if duplicate_ip_count > 0:
            flagged_anomalies.append(f"Suspicious IP concentration: {duplicate_ip_count} IP addresses submitted > 5 votes.")
            fraud_risk_score += min(duplicate_ip_count * 10.0, 20.0)

        # Cap score at 100%
        fraud_risk_score = round(min(fraud_risk_score, 100.0), 2)

        # Determine Risk Level
        if fraud_risk_score < 15.0:
            risk_level = "Low"
        elif fraud_risk_score < 40.0:
            risk_level = "Medium"
        elif fraud_risk_score < 70.0:
            risk_level = "High"
        else:
            risk_level = "Critical"

        if not flagged_anomalies:
            flagged_anomalies.append("Normal voting velocity and zero suspicious patterns detected.")

        return {
            "fraud_risk_score": fraud_risk_score,
            "risk_level": risk_level,
            "flagged_anomalies": flagged_anomalies,
            "details": {
                "total_votes": total_votes,
                "rapid_burst_count": rapid_burst_count,
                "duplicate_ip_count": duplicate_ip_count,
                "double_voting_attempts": double_voting_attempts
            }
        }

ai_fraud_service = AIFraudService()
