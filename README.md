# 🛡️ Blockchain Voting System

A production-quality, secure, transparent, full-stack **Blockchain Voting System** featuring a custom Python cryptographic engine (SHA-256, Proof-of-Work, Merkle Trees, ECDSA Digital Signatures), FastAPI backend, React 19 + Tailwind CSS frontend, AI Fraud Radar, real-time WebSockets, and downloadable QR code receipts.

---

## 🌟 Key Features

- **Custom Python Blockchain Engine**: Built from scratch using standard cryptographic primitives (SHA-256, Proof-of-Work, Merkle Trees, ECDSA SECP256R1, Block Signatures).
- **AES-256 GCM Vote Payload Encryption**: Ensures vote secrecy while allowing public ledger auditability.
- **Role-Based Access Control (RBAC)**:
  - 👑 **Admin**: Election CRUD, Candidate management, Bulk CSV Voter Import, System Metrics, Audit Logs.
  - 🗳️ **Voter**: Active election listing, Candidate profiles, 1-click encrypted voting, downloadable QR Receipts, Receipt Verification tool.
  - 👁️ **Observer**: Public transparency dashboard, Live Recharts vote tallies, Blockchain Explorer, Audit Log viewer.
- **AI Fraud Radar Module**: Analyzes vote velocity bursts, IP concentration, and duplicate vote attempts to compute a synthetic Fraud Risk Score (0 - 100%).
- **Real-Time WebSockets**: Live broadcast of vote counts, block mining, and election status updates.
- **Modern React 19 UI**: Built with Vite, Tailwind CSS, Lucide Icons, Recharts, Framer Motion, and Dark/Light mode support.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.12+
- Node.js 20+

---

### 1. Backend Setup (FastAPI & Blockchain)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
- API Documentation available at: `http://localhost:8000/docs`

---

### 2. Frontend Setup (React 19 + Vite)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
- Application UI available at: `http://localhost:3000`

---

## 🔑 Demo Seed Accounts

Upon first launch, the database automatically seeds demo accounts for testing:

| Role | Username | Email | Password |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin@blockchainvoting.org` | `Admin123!` |
| **Voter** | `voter1` | `voter@blockchainvoting.org` | `Voter123!` |
| **Observer** | `observer1` | `observer@blockchainvoting.org` | `Observer123!` |

---

## 🐳 Docker Deployment

To launch the full stack with Docker Compose:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## 🧪 Running Automated Tests

Run backend cryptographic & blockchain unit tests with pytest:

```bash
PYTHONPATH=. pytest backend/tests
```

---

## 📁 Project Structure

```text
blockchain-voting-system/
├── backend/
│   ├── app/
│   │   ├── api/             # REST Endpoints (Auth, Elections, Votes, Blockchain, Admin, AI, Observer)
│   │   ├── core/            # Security (JWT, bcrypt, AES-256), Settings, Database Session
│   │   ├── models/          # SQLAlchemy DB Models
│   │   ├── schemas/         # Pydantic Schemas
│   │   ├── services/        # Blockchain Service & AI Fraud Radar
│   │   ├── websockets/      # WebSocket Connection Manager
│   │   └── main.py          # FastAPI Entrypoint & Database Seeder
│   ├── blockchain/          # Custom Python Blockchain Engine (SHA-256, PoW, Merkle Tree, ECDSA)
│   ├── tests/               # Pytest Suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, Sidebar, QRCodeModal
│   │   ├── context/         # AuthContext, ThemeContext
│   │   ├── pages/           # Admin, Election, Voter, Receipt, Explorer, Observer, AI Fraud
│   │   ├── services/        # Axios API Client
│   │   └── types/           # TypeScript Types
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/                    # Architecture, Database Schema, Security Specs
├── .github/workflows/ci.yml # GitHub Actions CI Workflow
├── docker-compose.yml
└── README.md
```

---

## 📄 License
MIT License. Free for educational, Major TYBSc CS/AI-ML project, and portfolio use.
