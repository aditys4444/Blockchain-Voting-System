import sys
import os
import datetime

# Ensure backend directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base, SessionLocal
from .models import models
from .api import auth, elections, votes, blockchain, admin, ai, observer
from .services.blockchain_service import blockchain_service
from .websockets.manager import manager
from .core.security import get_password_hash

# Create Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(elections.router, prefix=settings.API_V1_STR)
app.include_router(votes.router, prefix=settings.API_V1_STR)
app.include_router(blockchain.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(observer.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Initialize Blockchain ledger sync
        blockchain_service.initialize_from_db(db)

        # Seed initial admin accounts
        for admin_email, admin_uname, admin_pwd in [
            ("admin@blockchainvoting.org", "admin", "Admin123!"),
            ("admin@voting.edu", "admin_edu", "admin123")
        ]:
            if not db.query(models.User).filter(models.User.email == admin_email).first():
                db.add(models.User(
                    email=admin_email,
                    username=admin_uname,
                    hashed_password=get_password_hash(admin_pwd),
                    role="admin"
                ))

        # Seed initial voter accounts
        for voter_email, voter_uname, voter_pwd in [
            ("voter@blockchainvoting.org", "voter1", "Voter123!"),
            ("voter1@voting.edu", "voter_edu", "voter123")
        ]:
            if not db.query(models.User).filter(models.User.email == voter_email).first():
                db.add(models.User(
                    email=voter_email,
                    username=voter_uname,
                    hashed_password=get_password_hash(voter_pwd),
                    role="voter"
                ))

        # Seed initial observer accounts
        for obs_email, obs_uname, obs_pwd in [
            ("observer@blockchainvoting.org", "observer1", "Observer123!"),
            ("observer@voting.edu", "observer_edu", "observer123")
        ]:
            if not db.query(models.User).filter(models.User.email == obs_email).first():
                db.add(models.User(
                    email=obs_email,
                    username=obs_uname,
                    hashed_password=get_password_hash(obs_pwd),
                    role="observer"
                ))

        db.commit()

        # Seed Demo Election if none exists
        demo_election = db.query(models.Election).first()
        if not demo_election:
            admin_ref = db.query(models.User).filter(models.User.role == "admin").first()
            demo_election = models.Election(
                title="General Presidential Election 2026",
                description="Official decentralised blockchain election for 2026 leadership.",
                status="active",
                start_time=datetime.datetime.utcnow(),
                end_time=datetime.datetime.utcnow() + datetime.timedelta(days=7),
                created_by=admin_ref.id if admin_ref else 1
            )
            db.add(demo_election)
            db.commit()
            db.refresh(demo_election)

            c1 = models.Candidate(
                election_id=demo_election.id,
                name="Dr. Alex Rivera",
                party="Progressive Tech Party",
                manifesto="Focusing on AI innovation, digital rights, and sustainable green technology.",
                avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"
            )
            c2 = models.Candidate(
                election_id=demo_election.id,
                name="Elena Rostova",
                party="Global Unity Alliance",
                manifesto="Transparency, decentralised governance, economic prosperity, and privacy protection.",
                avatar_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80"
            )
            db.add(c1)
            db.add(c2)
            db.commit()

    finally:
        db.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep socket alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
def root():
    return {
        "message": "Blockchain Voting System API is running smoothly.",
        "docs": "/docs",
        "health": "OK"
    }
