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

        # Seed initial admin user if no admin exists
        admin_user = db.query(models.User).filter(models.User.role == "admin").first()
        if not admin_user:
            admin_user = models.User(
                email="admin@blockchainvoting.org",
                username="admin",
                hashed_password=get_password_hash("Admin123!"),
                role="admin"
            )
            db.add(admin_user)

        # Seed initial voter user
        voter_user = db.query(models.User).filter(models.User.role == "voter").first()
        if not voter_user:
            voter_user = models.User(
                email="voter@blockchainvoting.org",
                username="voter1",
                hashed_password=get_password_hash("Voter123!"),
                role="voter"
            )
            db.add(voter_user)

        # Seed initial observer user
        observer_user = db.query(models.User).filter(models.User.role == "observer").first()
        if not observer_user:
            observer_user = models.User(
                email="observer@blockchainvoting.org",
                username="observer1",
                hashed_password=get_password_hash("Observer123!"),
                role="observer"
            )
            db.add(observer_user)

        db.commit()

        # Seed Demo Election if none exists
        demo_election = db.query(models.Election).first()
        if not demo_election:
            demo_election = models.Election(
                title="General Presidential Election 2026",
                description="Official decentralised blockchain election for 2026 leadership.",
                status="active",
                start_time=datetime.datetime.utcnow(),
                end_time=datetime.datetime.utcnow() + datetime.timedelta(days=7),
                created_by=admin_user.id
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
