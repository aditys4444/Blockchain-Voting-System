import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def create_pdf(filename="docs/Blockchain_Voting_System_SRS.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0284c7')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor('#0f172a')
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.HexColor('#0369a1')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        spaceAfter=3
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e293b')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # ================= COVER / TITLE PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Software Requirements Specification (SRS)", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Blockchain Voting System — Major Project", subtitle_style))
    story.append(Spacer(1, 30))

    meta_data = [
        [Paragraph("<b>Document Version:</b>", table_cell), Paragraph("1.0 Final Draft", table_cell)],
        [Paragraph("<b>Prepared By:</b>", table_cell), Paragraph("TYBSc Computer Science / AI-ML Project Team", table_cell)],
        [Paragraph("<b>Institution:</b>", table_cell), Paragraph("Thakur Ramnarayan College of Arts & Commerce (TRCAC)", table_cell)],
        [Paragraph("<b>Date:</b>", table_cell), Paragraph("August 2026", table_cell)],
        [Paragraph("<b>Scope:</b>", table_cell), Paragraph("Full-Stack Decoupled Architecture (FastAPI + React 19)", table_cell)],
        [Paragraph("<b>Status:</b>", table_cell), Paragraph("Production-Ready Release", table_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 370])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))

    # Table of Contents
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=10))

    toc_items = [
        "1. Introduction (Purpose, Scope, Definitions, References, Overview)",
        "2. Overall Description (Product Perspective, Functions, User Classes, Constraints)",
        "3. User Roles & Characteristics (Admin, Voter, Observer)",
        "4. Functional Requirements (Auth, Election, Vote, Blockchain, Observer, AI Fraud)",
        "5. Non-Functional Requirements (Performance, Security, Reliability, Usability, Scalability)",
        "6. System Constraints & Assumptions",
        "7. External Interface Requirements (UI, Hardware, Software, Communication)",
        "8. Data Requirements (Data Entities, Retention, Integrity)",
        "9. UML Diagrams & Architecture Diagrams Set (Use Case, Class, Sequence, ER)",
        "10. Architecture Design Document (ADD) & Key Decisions Matrix"
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # ================= SECTION 1: INTRODUCTION =================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))
    
    story.append(Paragraph("1.1 Purpose", h2_style))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) describes the complete functional, non-functional, "
        "and architectural requirements for the <b>Blockchain Voting System</b>. This document serves as the primary "
        "engineering contract for developer teams, academic evaluators, security auditors, and system administrators.",
        body_style
    ))

    story.append(Paragraph("1.2 Scope", h2_style))
    story.append(Paragraph(
        "The Blockchain Voting System is a modern web-based platform designed to conduct tamper-evident digital elections. "
        "It features a custom Python cryptographic blockchain engine, role-based access control, AES-256 GCM vote payload "
        "encryption, ECDSA SECP256R1 digital signatures, real-time WebSockets analytics, an AI Fraud Radar module, and downloadable QR code receipts.",
        body_style
    ))

    # Scope Table
    scope_data = [
        [Paragraph("Role / User Class", table_header), Paragraph("Key Capabilities & Module Privileges", table_header)],
        [Paragraph("Admin", table_cell), Paragraph("Full election creation, candidate studio, bulk voter CSV import, system metrics, audit logs, blockchain health.", table_cell)],
        [Paragraph("Voter", table_cell), Paragraph("View active elections, cast 1-click encrypted vote, download QR receipts, verify vote hash on ledger.", table_cell)],
        [Paragraph("Observer", table_cell), Paragraph("Read-only transparency desk, live Recharts vote tallies, blockchain block explorer, AI fraud radar.", table_cell)],
    ]
    t_scope = Table(scope_data, colWidths=[120, 380])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffffff')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 Definitions & Acronyms", h2_style))
    acronyms_data = [
        [Paragraph("Term", table_header), Paragraph("Definition", table_header)],
        [Paragraph("SRS", table_cell), Paragraph("Software Requirements Specification", table_cell)],
        [Paragraph("PoW", table_cell), Paragraph("Proof-of-Work mining consensus algorithm", table_cell)],
        [Paragraph("ECDSA", table_cell), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1)", table_cell)],
        [Paragraph("AES-256 GCM", table_cell), Paragraph("Advanced Encryption Standard with Galois/Counter Mode", table_cell)],
        [Paragraph("JWT", table_cell), Paragraph("JSON Web Token for stateless authorization", table_cell)],
        [Paragraph("RBAC", table_cell), Paragraph("Role-Based Access Control", table_cell)],
        [Paragraph("Merkle Tree", table_cell), Paragraph("Cryptographic hash tree aggregating block transactions", table_cell)],
    ]
    t_acr = Table(acronyms_data, colWidths=[100, 400])
    t_acr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_acr)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.4 Overview", h2_style))
    story.append(Paragraph(
        "The system is structured into three decoupled tiers: a React 19 + Vite frontend Single Page Application (SPA), "
        "a FastAPI (Python 3.12) REST API backend connected to SQLite / PostgreSQL, and an in-memory custom SHA-256 Blockchain ledger engine.",
        body_style
    ))

    story.append(PageBreak())

    # ================= SECTION 2: OVERALL DESCRIPTION =================
    story.append(Paragraph("2. Overall Description", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("2.1 Product Perspective", h2_style))
    story.append(Paragraph(
        "The Blockchain Voting System operates as a standalone full-stack web application replacing paper-based ballot casting. "
        "It enforces voter anonymity while providing verifiable audit trails via public block hashes, Merkle roots, and QR receipts.",
        body_style
    ))

    story.append(Paragraph("2.2 Product Functions (High-Level)", h2_style))
    functions = [
        "1. User Authentication & JWT Authorization — Secure role logins (Admin, Voter, Observer) with bcrypt password hashing.",
        "2. Election Management — Admin creates, edits, activates, schedules, and closes elections.",
        "3. Candidate Management — Admin creates candidate profiles with manifesto details and avatar URLs.",
        "4. Bulk Voter Import — Admin uploads CSV files to enroll voters in bulk.",
        "5. Vote Casting — Single vote per user per election enforced via database constraints and voter cryptographic hash.",
        "6. AES-256 Vote Payload Encryption — Candidate selections encrypted prior to block inclusion.",
        "7. ECDSA Digital Signature Signing — Transactions signed using single-use voter ECDSA key pairs.",
        "8. Proof-of-Work Block Mining — Mined blocks aggregate queued transactions with SHA-256 difficulty targets.",
        "9. QR Code Receipt Generation — Downloadable receipts containing receipt hash, block index, and transaction hash.",
        "10. Blockchain Explorer — Public block browser, transaction search, and 1-click ledger tamper auditor.",
        "11. AI Fraud Radar — Analyzes vote velocity bursts (<2s), duplicate IP concentration, and flags threat scores (0-100%).",
        "12. Real-Time WebSockets — Live broadcast of vote tallies, block mining events, and active standings."
    ]
    for func in functions:
        story.append(Paragraph(func, bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 Operating Environment", h2_style))
    env_data = [
        [Paragraph("Component", table_header), Paragraph("Specification", table_header)],
        [Paragraph("Client Browser", table_cell), Paragraph("Modern web browsers (Chrome, Firefox, Edge, Safari)", table_cell)],
        [Paragraph("Frontend Runtime", table_cell), Paragraph("Node.js v20+, Vite 5.x, React 19, Tailwind CSS 3.4", table_cell)],
        [Paragraph("Backend Server", table_cell), Paragraph("Python 3.12+, FastAPI 0.111+, Uvicorn ASGI Server", table_cell)],
        [Paragraph("Database Engine", table_cell), Paragraph("SQLite (dev mode) / PostgreSQL (production mode)", table_cell)],
        [Paragraph("Deployment Containers", table_cell), Paragraph("Docker, Docker Compose, GitHub Actions CI/CD", table_cell)],
    ]
    t_env = Table(env_data, colWidths=[120, 380])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_env)

    story.append(PageBreak())

    # ================= SECTION 3: USER ROLES & CHARACTERISTICS =================
    story.append(Paragraph("3. User Roles & Characteristics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    roles_data = [
        [Paragraph("User Role", table_header), Paragraph("Technical Level", table_header), Paragraph("Key Responsibilities & System Privileges", table_header)],
        [Paragraph("Admin", table_cell), Paragraph("Moderate to High", table_cell), Paragraph("Full administrative control. Creates elections, manages candidates, uploads CSV voter lists, views system metrics, monitors blockchain health, reviews audit logs.", table_cell)],
        [Paragraph("Voter", table_cell), Paragraph("Basic to Moderate", table_cell), Paragraph("Registered eligible voter. Views active elections, casts single encrypted vote, generates QR code receipt, verifies receipt hash on ledger.", table_cell)],
        [Paragraph("Observer", table_cell), Paragraph("Basic to High", table_cell), Paragraph("Public auditor. Read-only access to live election standings, vote percentage charts, block explorer, tamper verification, and AI fraud radar.", table_cell)],
    ]
    t_roles = Table(roles_data, colWidths=[80, 100, 320])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0369a1')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_roles)

    story.append(Spacer(1, 15))

    # ================= SECTION 4: FUNCTIONAL REQUIREMENTS =================
    story.append(Paragraph("4. Functional Requirements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    fr_items = [
        ("FR-AUTH-01: User Registration & Login", "System allows registration and login using email/username and password. Passwords are hashed using bcrypt with salt rounds. Returns JWT access and refresh tokens."),
        ("FR-AUTH-02: Role-Based Route Protection", "Frontend router and backend endpoints enforce role checking (admin, voter, observer). Unauthorized requests return HTTP 401/403."),
        ("FR-ELEC-01: Election Lifecycle Management", "Admin can create elections with title, description, start/end time. Elections transition through statuses: draft -> scheduled -> active -> closed."),
        ("FR-ELEC-02: Candidate Studio", "Admin can register candidates for an election with name, party affiliation, manifesto description, and avatar URL."),
        ("FR-VOTE-01: 1-Click Encrypted Voting", "Voters can select an active election candidate and submit a vote. Vote payload is encrypted using AES-256 GCM, signed with ECDSA SECP256R1, and mined into a block."),
        ("FR-VOTE-02: Anti-Double Voting Enforcement", "System checks if a voter has already cast a vote in the target election. Duplicate attempts are blocked and logged in audit trails."),
        ("FR-VOTE-03: Downloadable QR Receipt", "Upon vote confirmation, system generates a QR receipt containing receipt hash, block index, transaction hash, and voter anonymous hash."),
        ("FR-CHAIN-01: Proof-of-Work Block Mining", "Transactions are packaged into blocks. Miner computes SHA-256 block hash meeting difficulty target (e.g. leading zeros)."),
        ("FR-CHAIN-02: Merkle Tree Integrity", "Block header includes binary Merkle Root hash computed from contained transaction hashes. Recomputed during ledger audits."),
        ("FR-CHAIN-03: Blockchain Explorer", "Public endpoint allowing users to view mined blocks, search by block index or transaction hash, and trigger 1-click cryptographic chain verification."),
        ("FR-AI-01: AI Fraud Radar & Velocity Analysis", "AI service monitors vote submission velocity (<2s bursts), duplicate IP concentration, and double-vote attempts to output a 0-100% Fraud Risk Index.")
    ]

    for code, desc in fr_items:
        story.append(Paragraph(f"<b>{code}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # ================= SECTION 5: NON-FUNCTIONAL REQUIREMENTS =================
    story.append(Paragraph("5. Non-Functional Requirements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    nfr_data = [
        [Paragraph("Category", table_header), Paragraph("Requirement Specification", table_header)],
        [Paragraph("Performance", table_cell), Paragraph("API response time < 500ms for REST endpoints; block mining time < 2s under PoW difficulty 2.", table_cell)],
        [Paragraph("Security", table_cell), Paragraph("AES-256 GCM vote payload encryption, ECDSA digital signatures, bcrypt password hashing, JWT authorization.", table_cell)],
        [Paragraph("Reliability", table_cell), Paragraph("99.9% uptime. Immutable ledger guarantees 0 vote loss or unauthorized block modifications.", table_cell)],
        [Paragraph("Usability", table_cell), Paragraph("Responsive glassmorphism UI built with Tailwind CSS, Framer Motion animations, Dark/Light mode toggle.", table_cell)],
        [Paragraph("Scalability", table_cell), Paragraph("Stateless JWT architecture allows horizontal scaling; database compatible with SQLite and PostgreSQL.", table_cell)],
        [Paragraph("Maintainability", table_cell), Paragraph("Modular clean architecture separating API routes, database models, Pydantic schemas, and Blockchain services.", table_cell)],
    ]
    t_nfr = Table(nfr_data, colWidths=[110, 390])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_nfr)

    story.append(Spacer(1, 15))

    # ================= SECTION 6: SYSTEM CONSTRAINTS =================
    story.append(Paragraph("6. System Constraints", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    constraints = [
        "1. Blockchain difficulty is set to 2 zero-prefix target hashes for instant MVP demonstration without excessive CPU usage.",
        "2. Mock verification is used for MVP voter enrollment without requiring paid SMS/Email OTP gateways.",
        "3. Custom Python Blockchain operates as an in-memory/DB-persisted engine, designed so Ethereum/Solidity can be integrated later without altering core APIs.",
        "4. Single-vote policy is strictly enforced per user account per election."
    ]
    for c in constraints:
        story.append(Paragraph(c, bullet_style))

    story.append(Spacer(1, 15))

    # ================= SECTION 7: UML DIAGRAMS & ARCHITECTURE =================
    story.append(Paragraph("7. Architecture & System Flow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    story.append(Paragraph("7.1 Three-Tier Decoupled Model", h2_style))
    story.append(Paragraph(
        "<b>Tier 1 (Presentation Layer):</b> React 19 + Vite + Tailwind CSS Single Page Application.<br/>"
        "<b>Tier 2 (Application Layer):</b> FastAPI REST API + WebSockets connection manager + AI Fraud Radar.<br/>"
        "<b>Tier 3 (Data & Ledger Layer):</b> Custom SHA-256 Blockchain Engine + SQLAlchemy DB (SQLite / PostgreSQL).",
        body_style
    ))

    story.append(Paragraph("7.2 Cryptographic Voting Workflow", h2_style))
    workflow_steps = [
        "Step 1: Voter selects candidate in active election -> Frontend triggers POST /api/v1/votes/cast.",
        "Step 2: Backend verifies user hasn't voted & generates single-use ECDSA key pair and voter hash.",
        "Step 3: Vote choice encrypted using AES-256 GCM -> Digital signature generated using voter private key.",
        "Step 4: Transaction added to pool -> Proof-of-Work miner finds block nonce matching target difficulty.",
        "Step 5: Mined block appended to chain -> Database synced -> Real-time WebSocket event broadcast to dashboards.",
        "Step 6: QR Code Receipt generated containing receipt hash, block index, and transaction hash for verification."
    ]
    for step in workflow_steps:
        story.append(Paragraph(step, bullet_style))

    story.append(PageBreak())

    # ================= SECTION 8: DATA REQUIREMENTS & ER DIAGRAM =================
    story.append(Paragraph("8. Data Requirements & Schema", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    schema_data = [
        [Paragraph("Table / Entity", table_header), Paragraph("Primary Key", table_header), Paragraph("Key Fields & Constraints", table_header)],
        [Paragraph("users", table_cell), Paragraph("id", table_cell), Paragraph("email (unique), username (unique), hashed_password, role (admin/voter/observer), is_active", table_cell)],
        [Paragraph("elections", table_cell), Paragraph("id", table_cell), Paragraph("title, description, status (draft/scheduled/active/closed), start_time, end_time, created_by", table_cell)],
        [Paragraph("candidates", table_cell), Paragraph("id", table_cell), Paragraph("election_id (FK), name, party, manifesto, avatar_url, vote_count", table_cell)],
        [Paragraph("votes", table_cell), Paragraph("id", table_cell), Paragraph("user_id (FK), election_id (FK), candidate_id (FK), voter_hash, encrypted_vote, tx_hash (unique), block_index, receipt_hash (unique)", table_cell)],
        [Paragraph("blocks", table_cell), Paragraph("id", table_cell), Paragraph("index (unique), timestamp, previous_hash, hash (unique), nonce, merkle_root, signature", table_cell)],
        [Paragraph("transactions", table_cell), Paragraph("id", table_cell), Paragraph("tx_hash (unique), block_index, election_id, voter_hash, encrypted_vote, timestamp, signature", table_cell)],
        [Paragraph("audit_logs", table_cell), Paragraph("id", table_cell), Paragraph("user_id, user_email, action, details, ip_address, timestamp", table_cell)],
    ]
    t_schema = Table(schema_data, colWidths=[90, 60, 350])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_schema)

    story.append(Spacer(1, 20))
    story.append(Paragraph("9. Key Design Decisions Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f172a'), spaceAfter=8))

    decisions_data = [
        [Paragraph("#", table_header), Paragraph("Decision", table_header), Paragraph("Selected Choice", table_header), Paragraph("Rationale", table_header)],
        [Paragraph("1", table_cell), Paragraph("Cryptographic Ledger", table_cell), Paragraph("Custom Python Blockchain", table_cell), Paragraph("Zero gas fees, lightweight, complete control over block structure & PoW difficulty.", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Vote Secrecy", table_cell), Paragraph("AES-256 GCM Encryption", table_cell), Paragraph("Prevents plaintext vote choices from being visible in public block explorer.", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Voter Authenticity", table_cell), Paragraph("ECDSA SECP256R1 Signatures", table_cell), Paragraph("Asymmetric key pair ensures transaction cannot be forged or tampered.", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Real-Time Updates", table_cell), Paragraph("FastAPI WebSockets", table_cell), Paragraph("Instant push broadcasts of votes and block additions to dashboards without polling.", table_cell)],
        [Paragraph("5", table_cell), Paragraph("AI Threat Radar", table_cell), Paragraph("Heuristic Velocity Engine", table_cell), Paragraph("Detects vote bursts (<2s), duplicate IP clusters, and double-voting attempts.", table_cell)],
    ]
    t_dec = Table(decisions_data, colWidths=[20, 100, 120, 260])
    t_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dec)

    doc.build(story)
    print(f"Successfully generated PDF report at: {filename}")

if __name__ == "__main__":
    create_pdf()
