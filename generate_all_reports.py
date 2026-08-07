import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_pdf_reports():
    os.makedirs("docs", exist_ok=True)

    styles = getSampleStyleSheet()

    # Typography matching reference document
    cover_big_title = ParagraphStyle(
        'CoverBigTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    doc_header_title = ParagraphStyle(
        'DocHeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    doc_main_title = ParagraphStyle(
        'DocMainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    doc_sub_title = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.black
    )

    h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.black
    )

    h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.black
    )

    body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        spaceAfter=4,
        alignment=TA_LEFT,
        textColor=colors.black
    )

    bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=body,
        leftIndent=12,
        spaceAfter=3
    )

    th = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.black
    )

    td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.black
    )

    td_code = ParagraphStyle(
        'TDCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.black
    )

    # Common Table Style (Simple Black Borders like Reference Image)
    ref_table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    story = []

    # =========================================================================
    # PART 1: SRS (Software Requirements Specification) - Pages 1 to 16 Format
    # =========================================================================
    
    # Page 1: SRS Cover
    story.append(Spacer(1, 200))
    story.append(Paragraph("SRS", cover_big_title))
    story.append(PageBreak())

    # Page 2: Header & Meta & TOC
    story.append(Paragraph("Software Requirements Specification (SRS)", doc_header_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Blockchain Voting System", doc_main_title))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Cryptographic E-Voting & Ledger Module", doc_sub_title))
    story.append(Spacer(1, 15))

    meta_text = """
    <b>Document Version:</b> 1.0<br/>
    <b>Prepared By:</b> Student Project Team (TYBSc CS / AI-ML)<br/>
    <b>Institution:</b> Thakur Ramnarayan College of Arts & Commerce (TRCAC)<br/>
    <b>Date:</b> July 2026<br/>
    <b>Status:</b> Final Draft
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Table of Contents", h2))
    srs_toc = [
        "1. Introduction",
        "2. Overall Description",
        "3. User Roles & Characteristics",
        "4. Functional Requirements",
        "5. Non-Functional Requirements",
        "6. System Constraints",
        "7. External Interface Requirements",
        "8. Data Requirements"
    ]
    for idx, item in enumerate(srs_toc, 1):
        story.append(Paragraph(f"&nbsp;&nbsp;{item}", body))

    story.append(Spacer(1, 15))

    # 1. Introduction
    story.append(Paragraph("1. Introduction", h1))
    story.append(Paragraph("1.1 Purpose", h2))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the "
        "<b>Blockchain Voting System — E-Voting Module</b>. It is intended as a reference for the student development team, "
        "instructors, and any stakeholders involved in reviewing, testing, or extending the system.",
        body
    ))

    story.append(Paragraph("1.2 Scope", h2))
    story.append(Paragraph(
        "The <b>Blockchain Voting System</b> is a web-based platform designed to streamline secure and tamper-evident election processes "
        "at Thakur Ramnarayan College of Arts & Commerce. This document covers the decentralized voting portion of the system, "
        "which manages elections across degree programs:",
        body
    ))

    # Program Classes Table
    prog_data = [
        [Paragraph("Program", th), Paragraph("Classes", th)],
        [Paragraph("B.Sc (Computer Science)", td), Paragraph("FYBScCS, SYBScCS, TYBScCS", td)],
        [Paragraph("B.Sc (Information Technology)", td), Paragraph("FYBScIT, SYBScIT, TYBScIT", td)],
        [Paragraph("Bachelor of Arts", td), Paragraph("FYBA, SYBA, TYBA", td)],
        [Paragraph("BAMMC", td), Paragraph("FYBAMMC, SYBAMMC, TYBAMMC", td)],
        [Paragraph("Bachelor of Management Studies", td), Paragraph("FYBMS, SYBMS, TYBMS", td)],
        [Paragraph("Bachelor of Commerce", td), Paragraph("FYBCom, SYBCom, TYBCom", td)],
        [Paragraph("Bachelor of Accounting & Finance", td), Paragraph("FYBAF, SYBAF, TYBAF", td)],
    ]
    t_prog = Table(prog_data, colWidths=[200, 300])
    t_prog.setStyle(ref_table_style)
    story.append(t_prog)
    story.append(Spacer(1, 10))

    story.append(Paragraph("The system has three user roles: <b>Admin</b>, <b>Voter</b>, and <b>Observer</b>, each with distinct dashboards and privileges.", body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("1.3 Definitions & Acronyms", h2))
    
    terms_data = [
        [Paragraph("Term", th), Paragraph("Definition", th)],
        [Paragraph("BVS", td), Paragraph("Blockchain Voting System", td)],
        [Paragraph("TRCAC", td), Paragraph("Thakur Ramnarayan College of Arts & Commerce", td)],
        [Paragraph("PoW", td), Paragraph("Proof-of-Work mining algorithm", td)],
        [Paragraph("ECDSA", td), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1)", td)],
        [Paragraph("JWT", td), Paragraph("JSON Web Token — used for session authentication", td)],
        [Paragraph("API", td), Paragraph("Application Programming Interface", td)],
        [Paragraph("CRUD", td), Paragraph("Create, Read, Update, Delete", td)],
        [Paragraph("AES-256", td), Paragraph("Advanced Encryption Standard with 256-bit key", td)],
    ]
    t_terms = Table(terms_data, colWidths=[120, 380])
    t_terms.setStyle(ref_table_style)
    story.append(t_terms)

    story.append(Spacer(1, 10))
    story.append(Paragraph("1.4 References", h2))
    story.append(Paragraph("• Project Codebase: blockchain-voting-system (GitHub Repository)", bullet))
    story.append(Paragraph("• Security Documentation: SECURITY_SPECS.md", bullet))
    story.append(Paragraph("• Database Schema Documentation: DATABASE_SCHEMA.md", bullet))
    story.append(Paragraph("• System Architecture Documentation: SYSTEM_ARCHITECTURE.md", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("1.5 Overview", h2))
    story.append(Paragraph("The Blockchain Voting System is divided into two main logical layers:", body))
    story.append(Paragraph("1. <b>Frontend</b> — A React + Vite Single Page Application (SPA) with Tailwind CSS.", bullet))
    story.append(Paragraph("2. <b>Backend</b> — A FastAPI (Python 3.12) REST API connected to SQLite / PostgreSQL database and custom Python Blockchain Engine.", bullet))

    story.append(PageBreak())

    # 2. Overall Description
    story.append(Paragraph("2. Overall Description", h1))
    story.append(Paragraph("2.1 Product Perspective", h2))
    story.append(Paragraph(
        "The Blockchain Voting System is a standalone web application that replaces manual, paper-based voting processes. "
        "The system is intended to be used by students, faculty, and administrators of TRCAC.<br/><br/>"
        "The system integrates with:<br/>"
        "• <b>SQLite / PostgreSQL</b> — relational database for app data<br/>"
        "• <b>Custom Python Blockchain</b> — in-memory SHA-256 ledger<br/>"
        "• <b>FastAPI WebSockets</b> — real-time vote push updates",
        body
    ))

    story.append(Paragraph("2.2 Product Functions (High-Level)", h2))
    high_funcs = [
        "1. User Account Management — Admin creates voter and observer accounts; role-based login",
        "2. Election Management — Admin creates, schedules, activates, and closes elections",
        "3. Candidate Management — Admin creates candidate profiles with manifesto details",
        "4. Bulk Voter Enrollment — Admin bulk-enrolls voters via CSV upload",
        "5. 1-Click Encrypted Voting — Voter casts single vote encrypted with AES-256 GCM",
        "6. Digital Signature Signing — Transactions signed using single-use voter ECDSA key pairs",
        "7. Proof-of-Work Block Mining — Transactions packaged into blocks with SHA-256 difficulty targets",
        "8. Downloadable QR Receipt — Generates printable receipt containing receipt hash and block index",
        "9. Blockchain Explorer — Public block browser, transaction search, and 1-click ledger auditor",
        "10. AI Fraud Radar — Analyzes vote velocity bursts (<2s), duplicate IP clusters, and threat scores",
        "11. Live Transparency Dashboard — Observer views live Recharts standings and vote percentages"
    ]
    for hf in high_funcs:
        story.append(Paragraph(hf, bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 User Classes", h2))
    user_class_data = [
        [Paragraph("User Class", th), Paragraph("Description", th)],
        [Paragraph("Admin", td), Paragraph("Full control of the system. Creates accounts, manages elections, candidate profiles, and bulk voter data.", td)],
        [Paragraph("Voter", td), Paragraph("Casts votes in active elections, generates QR receipts, and verifies vote hash on blockchain ledger.", td)],
        [Paragraph("Observer", td), Paragraph("Read-only access. Watches live results, inspects block explorer, verifies chain integrity, and views AI fraud alerts.", td)],
    ]
    t_uc = Table(user_class_data, colWidths=[120, 380])
    t_uc.setStyle(ref_table_style)
    story.append(t_uc)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.4 Operating Environment", h2))
    story.append(Paragraph("• <b>Client Side:</b> Modern web browser (Chrome, Firefox, Edge, Safari)", bullet))
    story.append(Paragraph("• <b>Server Side:</b> Python 3.12+, FastAPI 0.111+, Uvicorn 0.30+", bullet))
    story.append(Paragraph("• <b>Database:</b> SQLite (local dev) / PostgreSQL (production)", bullet))
    story.append(Paragraph("• <b>Frontend Build Tool:</b> Vite 5.x", bullet))
    story.append(Paragraph("• <b>Deployment:</b> Docker, Docker Compose, GitHub Actions CI/CD", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.5 Design and Implementation Constraints", h2))
    story.append(Paragraph("• Frontend is built with <b>React 19</b> and <b>Tailwind CSS 3.4</b>", bullet))
    story.append(Paragraph("• Backend uses Python 3.12 with FastAPI REST framework", bullet))
    story.append(Paragraph("• JWT tokens expire in <b>24 hours</b> for session security", bullet))
    story.append(Paragraph("• Single-vote policy strictly enforced per voter per election", bullet))
    story.append(Paragraph("• CORS is strictly configured to allow only registered frontend URL", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.6 Assumptions and Dependencies", h2))
    story.append(Paragraph("• Users have stable internet connectivity.", bullet))
    story.append(Paragraph("• Every student possesses a valid institutional email.", bullet))
    story.append(Paragraph("• Custom Python Blockchain ledger service is operational.", bullet))

    story.append(PageBreak())

    # 3. User Roles & Characteristics
    story.append(Paragraph("3. User Roles & Characteristics", h1))
    story.append(Paragraph("3.1 Admin", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Moderate; expected to use a web-based admin dashboard", bullet))
    story.append(Paragraph("• <b>Access level:</b> Full system access", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> Create voter accounts, manage elections, bulk voter enrollment, view audit logs", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'admin')", bullet))

    story.append(Paragraph("3.2 Voter", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Basic to moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Scoped to assigned active elections", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> View candidates, cast encrypted vote, download QR receipt, verify hash", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'voter')", bullet))

    story.append(Paragraph("3.3 Observer", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Basic to moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Read-only access to public transparency metrics", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> View live results, inspect block ledger, audit chain, view AI fraud alerts", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'observer')", bullet))

    story.append(Spacer(1, 10))

    # 4. Functional Requirements
    story.append(Paragraph("4. Functional Requirements", h1))
    story.append(Paragraph("4.1 Authentication & Authorization Module", h2))
    
    fr_list_auth = [
        ("FR-AUTH-01: User Login", "The system shall allow admin, voters, and observers to log in using email/username and password.", "Email/Username, Password", "System searches user record and verifies password using bcrypt. Returns JWT token.", "JWT access token + user profile data", "24 hours", "Invalid credentials -> HTTP 400"),
        ("FR-AUTH-02: Admin User Creation", "Only authenticated admins can create new user accounts.", "Username, email, password, role (voter/observer)", "Admin endpoint creates user record.", "New user account created", "N/A", "Duplicate email -> HTTP 400"),
        ("FR-AUTH-03: Logout", "Users can log out, clearing local storage JWT token.", "Logout action", "Token removed from client storage.", "User redirected to /login", "N/A", "N/A"),
    ]
    for code, desc, inp, proc, out, exp, err in fr_list_auth:
        story.append(Paragraph(f"<b>{code}</b>", h2))
        story.append(Paragraph(f"• <b>Description:</b> {desc}", bullet))
        if inp != "N/A": story.append(Paragraph(f"• <b>Input:</b> {inp}", bullet))
        story.append(Paragraph(f"• <b>Process:</b> {proc}", bullet))
        if out != "N/A": story.append(Paragraph(f"• <b>Output:</b> {out}", bullet))
        if exp != "N/A": story.append(Paragraph(f"• <b>Token Expiry:</b> {exp}", bullet))
        if err != "N/A": story.append(Paragraph(f"• <b>Error Cases:</b> {err}", bullet))

    story.append(Paragraph("4.2 Admin Dashboard Module", h2))
    fr_list_admin = [
        ("FR-ADMIN-01: Dashboard Overview", "Displays total elections, active elections, registered voters, total votes, blockchain health.", "GET /api/v1/admin/metrics"),
        ("FR-ADMIN-02: Election Management", "Admin can create, edit, activate, and close elections.", "POST /api/v1/elections, PUT /api/v1/elections/:id/status"),
        ("FR-ADMIN-03: Candidate Studio", "Admin can register candidate profiles with name, party, manifesto, and avatar URL.", "POST /api/v1/elections/:id/candidates"),
        ("FR-ADMIN-04: Bulk Voter Enrollment", "Admin can upload a CSV file to bulk-create voter accounts.", "POST /api/v1/admin/import-voters-csv"),
        ("FR-ADMIN-05: Audit Log View", "Admin can view immutable audit logs of all user actions.", "GET /api/v1/admin/audit-logs")
    ]
    for code, desc, route in fr_list_admin:
        story.append(Paragraph(f"<b>{code}</b>", h2))
        story.append(Paragraph(f"• <b>Description:</b> {desc}", bullet))
        story.append(Paragraph(f"• <b>Route:</b> <font name='Courier'>{route}</font>", bullet))

    story.append(PageBreak())

    story.append(Paragraph("4.3 Voter Dashboard Module", h2))
    fr_list_voter = [
        ("FR-VOTER-01: Active Elections List", "Voters can view all currently active elections and candidate profiles.", "GET /api/v1/elections"),
        ("FR-VOTER-02: 1-Click Encrypted Vote", "Voter casts vote encrypted with AES-256 GCM and signed with ECDSA key pair.", "POST /api/v1/votes/cast"),
        ("FR-VOTER-03: Anti-Double Voting", "Enforces single vote per user per election.", "POST /api/v1/votes/cast (Checks existing vote)"),
        ("FR-VOTER-04: Downloadable QR Receipt", "Displays downloadable QR receipt containing receipt hash and block index.", "GET /api/v1/votes/my-receipts"),
        ("FR-VOTER-05: Receipt Verification", "Voters can verify any receipt hash against blockchain ledger.", "GET /api/v1/votes/verify-receipt/:hash")
    ]
    for code, desc, route in fr_list_voter:
        story.append(Paragraph(f"<b>{code}</b>", h2))
        story.append(Paragraph(f"• <b>Description:</b> {desc}", bullet))
        story.append(Paragraph(f"• <b>Route:</b> <font name='Courier'>{route}</font>", bullet))

    story.append(Paragraph("4.4 Custom Blockchain Module", h2))
    fr_list_bc = [
        ("FR-CHAIN-01: Block Mining", "Packages queued transactions into blocks meeting SHA-256 Proof-of-Work difficulty target.", "Internal Blockchain Engine"),
        ("FR-CHAIN-02: Merkle Tree Hash", "Header contains binary Merkle root hash calculated from transaction hashes.", "Internal Merkle Tree Generator"),
        ("FR-CHAIN-03: Ledger Explorer", "Public API allowing block browsing, transaction lookup, and 1-click chain audit.", "GET /api/v1/blockchain/blocks, GET /api/v1/blockchain/verify-chain")
    ]
    for code, desc, route in fr_list_bc:
        story.append(Paragraph(f"<b>{code}</b>", h2))
        story.append(Paragraph(f"• <b>Description:</b> {desc}", bullet))
        story.append(Paragraph(f"• <b>Route:</b> <font name='Courier'>{route}</font>", bullet))

    story.append(Paragraph("4.5 AI Fraud Radar Module", h2))
    story.append(Paragraph("<b>FR-AI-01: Fraud Risk Index</b>", h2))
    story.append(Paragraph("• <b>Description:</b> AI engine analyzes vote velocity bursts (<2s), duplicate IP clusters, and double-vote logs to output a threat index (0-100%).", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/ai/fraud-analysis/:election_id</font>", bullet))

    story.append(Spacer(1, 10))

    # 5. Non-Functional Requirements
    story.append(Paragraph("5. Non-Functional Requirements", h1))
    story.append(Paragraph("5.1 Performance", h2))
    nfr_perf_data = [
        [Paragraph("Metric", th), Paragraph("Requirement", th)],
        [Paragraph("API Response Time", td), Paragraph("< 500 milliseconds for REST endpoints under normal load", td)],
        [Paragraph("Block Mining", td), Paragraph("PoW block mined within 2 seconds for difficulty target = 2", td)],
        [Paragraph("Real-Time Push", td), Paragraph("WebSocket vote updates broadcast within 1 second", td)],
        [Paragraph("Concurrent Users", td), Paragraph("Supports at least 100 concurrent voters (student project scale)", td)],
    ]
    t_nfr_p = Table(nfr_perf_data, colWidths=[150, 350])
    t_nfr_p.setStyle(ref_table_style)
    story.append(t_nfr_p)

    story.append(Spacer(1, 10))
    story.append(Paragraph("5.2 Security", h2))
    sec_table_data = [
        [Paragraph("Requirement", th), Paragraph("Detail", th)],
        [Paragraph("Authentication", td), Paragraph("JWT Bearer tokens, 24-hour expiry", td)],
        [Paragraph("Password Storage", td), Paragraph("bcrypt password hashing with salt", td)],
        [Paragraph("Vote Confidentiality", td), Paragraph("AES-256 GCM symmetric vote payload encryption", td)],
        [Paragraph("Transaction Signing", td), Paragraph("ECDSA SECP256R1 asymmetric key pair digital signatures", td)],
        [Paragraph("CORS Protection", td), Paragraph("Whitelist-only: localhost:3000 and Vercel URL", td)],
        [Paragraph("Rate Limiting", td), Paragraph("Strict route limiters on login and vote casting endpoints", td)],
    ]
    t_sec = Table(sec_table_data, colWidths=[150, 350])
    t_sec.setStyle(ref_table_style)
    story.append(t_sec)

    story.append(Spacer(1, 10))
    story.append(Paragraph("5.3 Reliability & Usability", h2))
    story.append(Paragraph("• <b>Reliability:</b> System maintains 99.9% uptime. Immutable blockchain ledger guarantees zero vote deletion or modification.", bullet))
    story.append(Paragraph("• <b>Usability:</b> Responsive glassmorphic layout built with Tailwind CSS, supporting dark and light mode toggle.", bullet))
    story.append(Paragraph("• <b>Scalability:</b> Stateless JWT design allows backend scaling; relational DB supports SQLite and PostgreSQL.", bullet))

    story.append(PageBreak())

    # 6. System Constraints & 7. External Interface Requirements & 8. Data Requirements
    story.append(Paragraph("6. System Constraints", h1))
    story.append(Paragraph("1. Proof-of-Work difficulty target is set to 2 zero-prefix hashes for MVP efficiency.", bullet))
    story.append(Paragraph("2. Custom Python Blockchain operates in-memory synced to SQLite database.", bullet))
    story.append(Paragraph("3. Single vote policy strictly enforced per voter per election.", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("7. External Interface Requirements", h1))
    story.append(Paragraph("7.1 User Interfaces", h2))
    ui_table_data = [
        [Paragraph("Page", th), Paragraph("Role", th), Paragraph("Description", th)],
        [Paragraph("Login / Register", td), Paragraph("Public", td), Paragraph("Authentication portal with role selector", td)],
        [Paragraph("Admin Dashboard", td), Paragraph("Admin", td), Paragraph("Overview metrics, elections CRUD, CSV import, audit logs", td)],
        [Paragraph("Voter Dashboard", td), Paragraph("Voter", td), Paragraph("Active elections, 1-click vote casting, QR receipts", td)],
        [Paragraph("Observer Dashboard", td), Paragraph("Observer", td), Paragraph("Live Recharts standings, block explorer, AI fraud radar", td)],
        [Paragraph("Blockchain Explorer", td), Paragraph("Public", td), Paragraph("Mined blocks, transaction search, 1-click audit", td)],
    ]
    t_ui = Table(ui_table_data, colWidths=[120, 80, 300])
    t_ui.setStyle(ref_table_style)
    story.append(t_ui)

    story.append(Spacer(1, 10))
    story.append(Paragraph("7.2 Software & Communication Interfaces", h2))
    story.append(Paragraph("• <b>Protocol:</b> HTTPS (production), HTTP (local development)", bullet))
    story.append(Paragraph("• <b>Data Format:</b> JSON (REST API & WebSockets)", bullet))
    story.append(Paragraph("• <b>Auth Header:</b> Authorization: Bearer &lt;JWT_TOKEN&gt;", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Data Requirements", h1))
    story.append(Paragraph("8.1 Data Entities", h2))
    entity_data = [
        [Paragraph("Entity", th), Paragraph("Table", th), Paragraph("Key Fields", th)],
        [Paragraph("User", td), Paragraph("users", td), Paragraph("id, email, username, hashed_password, role, is_active", td)],
        [Paragraph("Election", td), Paragraph("elections", td), Paragraph("id, title, description, status, start_time, end_time", td)],
        [Paragraph("Candidate", td), Paragraph("candidates", td), Paragraph("id, election_id, name, party, manifesto, vote_count", td)],
        [Paragraph("Vote", td), Paragraph("votes", td), Paragraph("id, user_id, election_id, candidate_id, voter_hash, tx_hash, block_index, receipt_hash", td)],
        [Paragraph("Block", td), Paragraph("blocks", td), Paragraph("id, index, timestamp, previous_hash, hash, nonce, merkle_root, signature", td)],
        [Paragraph("Transaction", td), Paragraph("transactions", td), Paragraph("id, tx_hash, block_index, election_id, voter_hash, encrypted_vote, signature", td)],
        [Paragraph("AuditLog", td), Paragraph("audit_logs", td), Paragraph("id, user_id, user_email, action, details, ip_address, timestamp", td)],
    ]
    t_ent = Table(entity_data, colWidths=[90, 80, 330])
    t_ent.setStyle(ref_table_style)
    story.append(t_ent)

    story.append(PageBreak())

    # =========================================================================
    # PART 2: UML (UML Diagrams — Complete Set) - Pages 18 to 32 Format
    # =========================================================================
    story.append(Spacer(1, 200))
    story.append(Paragraph("UML", cover_big_title))
    story.append(PageBreak())

    story.append(Paragraph("UML Diagrams — Complete Set", doc_header_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Blockchain Voting System", doc_main_title))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Table of Contents", h2))
    uml_toc = [
        "1. Use Case Diagrams (Admin, Voter, Observer)",
        "2. Class Diagrams (User & Auth, Content & Block, Assessment & Vote)",
        "3. Sequence Diagram — Login Flow",
        "4. Sequence Diagram — Encrypted Vote & Block Mining Flow",
        "5. Sequence Diagram — Receipt Verification Flow",
        "6. Activity Diagram — AI Fraud Detection & Velocity Marking",
        "7. Component Diagram",
        "8. Entity-Relationship (ER) Diagram"
    ]
    for item in uml_toc:
        story.append(Paragraph(f"&nbsp;&nbsp;{item}", body))

    story.append(Spacer(1, 15))
    story.append(Paragraph("1. Use Case Diagrams", h1))
    story.append(Paragraph("1.1 Admin Use Cases", h2))
    story.append(Paragraph("Admin actor interacts with: Login/Logout, Create Election, Add Candidate, Bulk Enroll Voters CSV, View Dashboard Stats, View Audit Logs, Check Blockchain Health.", body))

    story.append(Paragraph("1.2 Voter Use Cases", h2))
    story.append(Paragraph("Voter actor interacts with: Login/Logout, View Active Elections, View Candidates, Cast Encrypted Vote, View QR Receipt, Verify Receipt Hash.", body))

    story.append(Paragraph("1.3 Observer Use Cases", h2))
    story.append(Paragraph("Observer actor interacts with: View Live Recharts Standings, Inspect Mined Blocks, Search Transaction, Trigger Chain Audit, View AI Fraud Alerts.", body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Class Diagrams", h1))
    story.append(Paragraph("2.1 User & Auth Classes", h2))
    story.append(Paragraph("<b>User Base Class:</b> +id, +email, +username, +hashed_password, +role<br/>"
                           "<b>Subclasses / Roles:</b> AdminUser, VoterUser, ObserverUser.", body))

    story.append(Paragraph("2.2 Content & Block Classes", h2))
    story.append(Paragraph("<b>Block Class:</b> +index, +timestamp, +previous_hash, +hash, +nonce, +merkle_root, +signature, +calculate_hash()<br/>"
                           "<b>Blockchain Engine Class:</b> +chain[], +pending_txs[], +mine_pending_transactions(), +is_chain_valid().", body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Sequence Diagrams", h1))
    story.append(Paragraph("3.1 Login Flow", h2))
    story.append(Paragraph("Voter -> React Frontend -> POST /api/v1/auth/login -> FastAPI API -> SQLAlchemy DB (verify bcrypt) -> Return JWT Token.", body))

    story.append(Paragraph("3.2 Encrypted Vote & Block Mining Flow", h2))
    story.append(Paragraph("Voter -> React Frontend -> AES-256 Encrypt -> ECDSA Sign -> POST /api/v1/votes/cast -> FastAPI -> Blockchain Engine (PoW Mine Block) -> DB Sync -> WebSocket Broadcast.", body))

    story.append(PageBreak())

    # =========================================================================
    # PART 3: ADD (Architecture Design Document) - Pages 33 to 53 Format
    # =========================================================================
    story.append(Spacer(1, 200))
    story.append(Paragraph("ADD", cover_big_title))
    story.append(PageBreak())

    story.append(Paragraph("Architecture Design Document (ADD)", doc_header_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Blockchain Voting System", doc_main_title))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Version: 1.0 | Date: July 2026 | Scope: Full-Stack Decoupled Architecture", doc_sub_title))
    story.append(Spacer(1, 15))

    story.append(Paragraph("1. Introduction & Architectural Goals", h1))
    arch_goals = [
        [Paragraph("Goal", th), Paragraph("Description", th)],
        [Paragraph("Separation of Concerns", td), Paragraph("UI never touches database directly — frontend React SPA and backend FastAPI REST API are fully decoupled.", td)],
        [Paragraph("Role-Based Security", td), Paragraph("Every protected endpoint enforces strict Admin / Voter / Observer role checks via JWT claims.", td)],
        [Paragraph("Stateless Auth", td), Paragraph("JWT-based authentication allows horizontal scaling across multiple backend worker instances.", td)],
        [Paragraph("Tamper Immutability", td), Paragraph("Votes are recorded in SHA-256 blocks with Merkle roots and Proof-of-Work headers.", td)],
        [Paragraph("Vote Secrecy", td), Paragraph("Candidate choices encrypted with AES-256 GCM prior to block inclusion.", td)],
    ]
    t_ag = Table(arch_goals, colWidths=[140, 360])
    t_ag.setStyle(ref_table_style)
    story.append(t_ag)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. System Context & External Systems", h1))
    actors_sys_data = [
        [Paragraph("Actor / System", th), Paragraph("Type", th), Paragraph("Role", th)],
        [Paragraph("Admin", td), Paragraph("User", td), Paragraph("Creates elections, candidate profiles, bulk voter enrollment, monitors metrics.", td)],
        [Paragraph("Voter", td), Paragraph("User", td), Paragraph("Casts encrypted vote, views active elections, generates QR receipt.", td)],
        [Paragraph("Observer", td), Paragraph("User", td), Paragraph("Monitors live Recharts standings, inspects block explorer, checks AI alerts.", td)],
        [Paragraph("SQLite / PostgreSQL", td), Paragraph("Database", td), Paragraph("Relational data store for user profiles, elections, and blocks.", td)],
        [Paragraph("Python Blockchain", td), Paragraph("Core Engine", td), Paragraph("SHA-256 PoW miner, Merkle tree generator, ECDSA signature verifier.", td)],
        [Paragraph("Vercel / Docker", td), Paragraph("Deployment", td), Paragraph("Static CDN frontend hosting & containerized ASGI backend runtime.", td)],
    ]
    t_as = Table(actors_sys_data, colWidths=[120, 80, 300])
    t_as.setStyle(ref_table_style)
    story.append(t_as)

    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Frontend Architecture (React 19 + Vite)", h1))
    fe_tech_data = [
        [Paragraph("Technology", th), Paragraph("Version", th), Paragraph("Role", th)],
        [Paragraph("React", td), Paragraph("19.0", td), Paragraph("UI Component Library", td)],
        [Paragraph("Vite", td), Paragraph("5.x", td), Paragraph("Build tool & HMR dev server", td)],
        [Paragraph("React Router DOM", td), Paragraph("6.x", td), Paragraph("Client-side declarative routing", td)],
        [Paragraph("Tailwind CSS", td), Paragraph("3.4", td), Paragraph("Utility-first styling & Dark Mode", td)],
        [Paragraph("Framer Motion", td), Paragraph("11.x", td), Paragraph("Smooth page animations", td)],
        [Paragraph("Recharts", td), Paragraph("2.x", td), Paragraph("Live vote distribution charts", td)],
        [Paragraph("Axios", td), Paragraph("1.x", td), Paragraph("HTTP client with JWT interceptors", td)],
    ]
    t_fe = Table(fe_tech_data, colWidths=[120, 80, 300])
    t_fe.setStyle(ref_table_style)
    story.append(t_fe)

    story.append(PageBreak())

    story.append(Paragraph("4. Backend Architecture (FastAPI + Python 3.12)", h1))
    be_tech_data = [
        [Paragraph("Technology", th), Paragraph("Version", th), Paragraph("Role", th)],
        [Paragraph("Python", td), Paragraph("3.12+", td), Paragraph("Server runtime environment", td)],
        [Paragraph("FastAPI", td), Paragraph("0.111+", td), Paragraph("High-performance ASGI web framework", td)],
        [Paragraph("SQLAlchemy", td), Paragraph("2.0+", td), Paragraph("Relational ORM database mapping", td)],
        [Paragraph("PyJWT", td), Paragraph("2.8+", td), Paragraph("JSON Web Token signing & decoding", td)],
        [Paragraph("bcrypt", td), Paragraph("4.1+", td), Paragraph("Salted password hashing", td)],
        [Paragraph("Cryptography", td), Paragraph("42.0+", td), Paragraph("ECDSA SECP256R1 & AES-256 GCM algorithms", td)],
        [Paragraph("WebSockets", td), Paragraph("12.0+", td), Paragraph("Real-time bidirectional event manager", td)],
    ]
    t_be = Table(be_tech_data, colWidths=[120, 80, 300])
    t_be.setStyle(ref_table_style)
    story.append(t_be)

    story.append(Spacer(1, 10))
    story.append(Paragraph("4.1 API Route Map", h2))
    api_map_data = [
        [Paragraph("Prefix", th), Paragraph("File", th), Paragraph("Key Endpoints", th)],
        [Paragraph("/api/v1/auth", td), Paragraph("auth.py", td), Paragraph("POST /login, POST /register, GET /me", td)],
        [Paragraph("/api/v1/elections", td), Paragraph("elections.py", td), Paragraph("GET /, POST /, PUT /:id/status, POST /:id/candidates", td)],
        [Paragraph("/api/v1/votes", td), Paragraph("votes.py", td), Paragraph("POST /cast, GET /my-receipts, GET /verify-receipt/:hash", td)],
        [Paragraph("/api/v1/blockchain", td), Paragraph("blockchain.py", td), Paragraph("GET /blocks, GET /status, GET /verify-chain", td)],
        [Paragraph("/api/v1/admin", td), Paragraph("admin.py", td), Paragraph("GET /metrics, POST /import-voters-csv, GET /audit-logs", td)],
        [Paragraph("/api/v1/ai", td), Paragraph("ai.py", td), Paragraph("GET /fraud-analysis/:election_id", td)],
        [Paragraph("/api/v1/observer", td), Paragraph("observer.py", td), Paragraph("GET /live-results/:election_id", td)],
    ]
    t_map = Table(api_map_data, colWidths=[110, 90, 300])
    t_map.setStyle(ref_table_style)
    story.append(t_map)

    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Key Design Decisions Matrix", h1))
    decisions_matrix = [
        [Paragraph("#", th), Paragraph("Decision", th), Paragraph("Choice", th), Paragraph("Rationale", th), Paragraph("Tradeoff", th)],
        [Paragraph("1", td), Paragraph("User storage", td), Paragraph("Single users table with role enum", td), Paragraph("Unified auth lookup without multi-table queries.", td), Paragraph("Requires role checks on every route.", td)],
        [Paragraph("2", td), Paragraph("Vote Secrecy", td), Paragraph("AES-256 GCM payload encryption", td), Paragraph("Prevents vote choices from showing plaintext on block explorer.", td), Paragraph("Requires server encryption key.", td)],
        [Paragraph("3", td), Paragraph("Voter Auth", td), Paragraph("ECDSA SECP256R1 Key Pairs", td), Paragraph("Digital signature guarantees vote cannot be forged.", td), Paragraph("Keypair generated per vote.", td)],
        [Paragraph("4", td), Paragraph("Real-Time", td), Paragraph("FastAPI WebSockets", td), Paragraph("Instant push broadcasts to live dashboards.", td), Paragraph("Active socket connection management.", td)],
        [Paragraph("5", td), Paragraph("AI Threat Radar", td), Paragraph("Heuristic Velocity Analysis", td), Paragraph("Detects bursts (<2s), duplicate IPs, double voting.", td), Paragraph("Thresholds require tuning.", td)],
    ]
    t_dec_m = Table(decisions_matrix, colWidths=[15, 80, 110, 160, 135])
    t_dec_m.setStyle(ref_table_style)
    story.append(t_dec_m)

    # Build PDF - Output All-In-One PDF Document
    pdf_path_all = "docs/Blockchain_Voting_System_All_In_One_Project_Report.pdf"
    pdf_path_full = "docs/Blockchain_Voting_System_Full_Project_Report.pdf"

    doc_all = SimpleDocTemplate(pdf_path_all, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    doc_all.build(story)
    print(f"Successfully generated All-In-One PDF report at: {pdf_path_all}")

    doc_full = SimpleDocTemplate(pdf_path_full, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    doc_full.build(story)
    print(f"Successfully generated Full PDF report at: {pdf_path_full}")

if __name__ == "__main__":
    build_pdf_reports()
