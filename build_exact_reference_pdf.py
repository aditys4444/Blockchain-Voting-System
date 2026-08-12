import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def generate_exact_reference_pdf(filename="docs/Blockchain_Voting_System_Project_Report.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Exact Typography Matching Reference Screenshots
    cover_style = ParagraphStyle(
        'RefCoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        alignment=TA_LEFT,
        spaceBefore=10,
        textColor=colors.black
    )

    doc_header = ParagraphStyle(
        'RefDocHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    doc_title = ParagraphStyle(
        'RefDocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.black
    )
    doc_main_title = doc_title

    doc_subtitle = ParagraphStyle(
        'RefDocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.black
    )

    meta_style = ParagraphStyle(
        'RefMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.black
    )

    h1 = ParagraphStyle(
        'RefH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=4,
        textColor=colors.black
    )

    h2 = ParagraphStyle(
        'RefH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=8,
        spaceAfter=3,
        textColor=colors.black
    )

    body = ParagraphStyle(
        'RefBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        spaceAfter=3,
        alignment=TA_LEFT,
        textColor=colors.black
    )

    bullet = ParagraphStyle(
        'RefBullet',
        parent=body,
        leftIndent=12,
        spaceAfter=2
    )

    th = ParagraphStyle(
        'RefTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.black
    )

    td = ParagraphStyle(
        'RefTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.black
    )

    code_font = ParagraphStyle(
        'RefCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black
    )

    # Clean Crisp Table Style (Black borders like Reference Image)
    ref_table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    story = []

    # =========================================================================
    # ========================== PART 1: SRS ==================================
    # =========================================================================

    # Page 1: SRS Cover (Exact match to Screenshot 1)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>SRS</b>", cover_style))
    story.append(PageBreak())

    # Page 2: Title, Metadata, TOC, 1. Introduction, 1.1 Purpose (Screenshot 2)
    story.append(Spacer(1, 15))
    story.append(Paragraph("Software Requirements Specification (SRS)", doc_header))
    story.append(Spacer(1, 15))
    story.append(Paragraph("TRCAC Blockchain Voting System (BVS)", doc_title))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Degree College Module", doc_subtitle))
    story.append(Spacer(1, 15))

    meta_text = """
    <b>Document Version:</b> 1.0<br/>
    <b>Prepared By:</b> Student Project Team<br/>
    <b>Institution:</b> TRCAC (Thakur Ramnarayan College of Arts & Commerce)<br/>
    <b>Date:</b> July 2026<br/>
    <b>Status:</b> Final Draft
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Table of Contents</b>", doc_title))
    srs_toc = [
        "1. &nbsp;Introduction",
        "2. &nbsp;Overall Description",
        "3. &nbsp;User Roles & Characteristics",
        "4. &nbsp;Functional Requirements",
        "5. &nbsp;Non-Functional Requirements",
        "6. &nbsp;System Constraints",
        "7. &nbsp;External Interface Requirements",
        "8. &nbsp;Data Requirements"
    ]
    for item in srs_toc:
        story.append(Paragraph(item, bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("1. Introduction", h1))
    story.append(Paragraph("1.1 Purpose", h2))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the "
        "<b>TRCAC Blockchain Voting System (BVS) — Degree College Module</b>. It is intended as a reference for the student "
        "development team, instructors, and any stakeholders involved in reviewing, testing, or extending the system.",
        body
    ))
    story.append(PageBreak())

    # Page 3: 1.2 Scope & Program Classes Table & Roles (Screenshot 3)
    story.append(Paragraph("1.2 Scope", h1))
    story.append(Paragraph(
        "The <b>TRCAC BVS</b> is a web-based platform designed to streamline secure and tamper-evident election activities at "
        "Thakur Ramnarayan College of Arts & Commerce. This document covers only the <b>Degree College</b> portion of the system, "
        "which manages the following degree programs:",
        body
    ))
    story.append(Spacer(1, 6))

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
    t_prog = Table(prog_data, colWidths=[220, 280])
    t_prog.setStyle(ref_table_style)
    story.append(t_prog)
    story.append(Spacer(1, 10))

    story.append(Paragraph("The system has three user roles: <b>Admin</b>, <b>Voter (Student)</b>, and <b>Observer (Faculty/Public)</b>, each with distinct dashboards and privileges.", body))
    story.append(PageBreak())

    # Page 4: 1.3 Definitions & Acronyms, 1.4 References, 1.5 Overview, 2. Overall Description (Screenshot 4)
    story.append(Paragraph("1.3 Definitions & Acronyms", h1))
    terms_data = [
        [Paragraph("Term", th), Paragraph("Definition", th)],
        [Paragraph("BVS", td), Paragraph("Blockchain Voting System", td)],
        [Paragraph("TRCAC", td), Paragraph("Thakur Ramnarayan College of Arts & Commerce", td)],
        [Paragraph("DC", td), Paragraph("Degree College", td)],
        [Paragraph("FY / SY / TY", td), Paragraph("First Year / Second Year / Third Year", td)],
        [Paragraph("JWT", td), Paragraph("JSON Web Token — used for session authentication", td)],
        [Paragraph("API", td), Paragraph("Application Programming Interface", td)],
        [Paragraph("CRUD", td), Paragraph("Create, Read, Update, Delete", td)],
        [Paragraph("PoW", td), Paragraph("Proof-of-Work mining consensus algorithm", td)],
        [Paragraph("ECDSA", td), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1)", td)],
    ]
    t_terms = Table(terms_data, colWidths=[120, 380])
    t_terms.setStyle(ref_table_style)
    story.append(t_terms)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.4 References", h2))
    story.append(Paragraph("• Project Codebase: trcac-blockchain-voting (GitHub Repository)", bullet))
    story.append(Paragraph("• DC Subject and Class List: DC class and candidate list.xlsx", bullet))
    story.append(Paragraph("• Security Documentation: SECURITY_SPECS.md", bullet))
    story.append(Paragraph("• Architecture Documentation: SYSTEM_ARCHITECTURE.md", bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("1.5 Overview", h2))
    story.append(Paragraph("The BVS is divided into two main logical layers:", body))
    story.append(Paragraph("9. &nbsp;<b>Frontend</b> — A React + Vite Single Page Application (SPA) deployed on Vercel", bullet))
    story.append(Paragraph("10. <b>Backend</b> — A FastAPI (Python 3.12) REST API connected to database and Blockchain Engine", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Overall Description", h1))
    story.append(Paragraph("2.1 Product Perspective", h2))
    story.append(Paragraph(
        "The TRCAC BVS Degree College module is a standalone web application that replaces manual, paper-based academic voting processes. "
        "The system is intended to be used by faculty members, students, and administrators of the degree college section of TRCAC.<br/><br/>"
        "The system integrates with:<br/>"
        "• <b>SQLite / PostgreSQL</b> — cloud database<br/>"
        "• <b>Custom Python Blockchain</b> — decentralized SHA-256 ledger<br/>"
        "• <b>FastAPI WebSockets</b> — real-time vote updates",
        body
    ))
    story.append(PageBreak())

    # Page 5: 2.2 Product Functions, 2.3 User Classes, 2.4 Operating Environment, 2.5 Constraints (Screenshot 5)
    story.append(Paragraph("2.2 Product Functions (High-Level)", h1))
    story.append(Paragraph("The following high-level capabilities are supported for the Degree College module:", body))
    high_funcs = [
        "11. User Account Management — Admin creates student and faculty accounts; role-based login",
        "12. Election Management — Admin publishes elections; students and faculty view elections",
        "13. Candidate Management — Admin manages candidate nominations per degree, year, and class",
        "14. 1-Click Encrypted Voting — Vote choices encrypted via AES-256 GCM before ledger submission",
        "15. Anti-Double Voting Enforcement — Single vote per student strictly enforced at database and blockchain layer",
        "16. Digital Signature Signing — Transactions signed using single-use voter ECDSA key pairs",
        "17. Proof-of-Work Block Mining — Mined blocks aggregate queued transactions with SHA-256 target difficulty",
        "18. Bulk Enrollment — Admin bulk-enrolls students via CSV upload",
        "19. Audit Log Tracking — System logs logins, vote events, and admin activities",
        "20. Blockchain Explorer — Public block browser, transaction search, and 1-click chain audit",
        "21. Settings / Password Management — Users can change their own passwords"
    ]
    for hf in high_funcs:
        story.append(Paragraph(hf, bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 User Classes", h1))
    uc_data = [
        [Paragraph("User Class", th), Paragraph("Description", th)],
        [Paragraph("Admin", td), Paragraph("Full control of the system. Creates accounts, manages elections, candidates, and bulk data.", td)],
        [Paragraph("DC Student (Voter)", td), Paragraph("Casts votes, generates QR receipts, views active elections, and verifies ledger hashes.", td)],
        [Paragraph("DC Faculty (Observer)", td), Paragraph("Monitors live election results, inspects block explorer, verifies chain, and views AI fraud alerts.", td)],
    ]
    t_uc = Table(uc_data, colWidths=[130, 370])
    t_uc.setStyle(ref_table_style)
    story.append(t_uc)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.4 Operating Environment", h1))
    story.append(Paragraph("• <b>Client Side:</b> Modern web browser (Chrome, Firefox, Edge, Safari)", bullet))
    story.append(Paragraph("• <b>Server Side:</b> Python 3.12+, FastAPI 0.111+, Uvicorn 0.30+", bullet))
    story.append(Paragraph("• <b>Database:</b> SQLite (local) / PostgreSQL (cloud-hosted)", bullet))
    story.append(Paragraph("• <b>Frontend Build Tool:</b> Vite 5.x / 7.x", bullet))
    story.append(Paragraph("• <b>Deployment:</b> Frontend -> Vercel; Backend -> Railway / Render (port 8000)", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.5 Design and Implementation Constraints", h1))
    story.append(Paragraph("• Frontend is built with <b>React 19</b> and <b>Tailwind CSS 3</b>", bullet))
    story.append(Paragraph("• Backend uses Python 3.12 with FastAPI REST framework", bullet))
    story.append(Paragraph("• JWT tokens expire in <b>24 hours</b> for security", bullet))
    story.append(PageBreak())

    # Page 6: Constraints continued, 2.6 Assumptions, 3. User Roles (Screenshot 6)
    story.append(Paragraph("• File uploads are limited to <b>10 MB</b> per file", bullet))
    story.append(Paragraph("• Allowed file types for bulk voter import: CSV", bullet))
    story.append(Paragraph("• Rate limiting is applied to all API endpoints", bullet))
    story.append(Paragraph("• CORS is strictly configured to allow only the registered frontend URL", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.6 Assumptions and Dependencies", h1))
    story.append(Paragraph("• Users have stable internet connectivity.", bullet))
    story.append(Paragraph("• Every student possesses a valid institutional email.", bullet))
    story.append(Paragraph("• Database service remains available.", bullet))
    story.append(Paragraph("• JWT authentication service is operational.", bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("3. User Roles & Characteristics", h1))
    story.append(Paragraph("3.1 Admin", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Moderate; expected to use a web-based admin dashboard", bullet))
    story.append(Paragraph("• <b>Access level:</b> Full system access", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> Create voter/faculty accounts, manage elections, bulk enrollment", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'admin')", bullet))

    story.append(Paragraph("3.2 Degree College Faculty (DC Faculty / Observer)", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Scoped to monitoring live standings and transparency metrics", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> View results, audit blockchain ledger, inspect AI fraud alerts", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'observer')", bullet))

    story.append(Paragraph("3.3 Degree College Student (DC Student / Voter)", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Basic to moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Scoped to their own class, year, and active election ballot", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> Cast encrypted vote, download QR receipt, verify receipt hash", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'voter')", bullet))
    story.append(PageBreak())

    # Page 7: Actor Use Cases Table & 4. Functional Requirements - Auth (Screenshot 7)
    actor_uc_data = [
        [Paragraph("Actor", th), Paragraph("Use Cases", th)],
        [Paragraph("Admin", td), Paragraph("Manage Users, Elections, Candidates, Bulk CSV Import", td)],
        [Paragraph("Faculty / Observer", td), Paragraph("Live Standings, Audit Ledger, Chain Verification, AI Fraud Alerts", td)],
        [Paragraph("Student / Voter", td), Paragraph("Cast Encrypted Vote, View Candidates, QR Receipt, Verify Hash", td)],
    ]
    t_auc = Table(actor_uc_data, colWidths=[120, 380])
    t_auc.setStyle(ref_table_style)
    story.append(t_auc)
    story.append(Spacer(1, 15))

    story.append(Paragraph("4. Functional Requirements", h1))
    story.append(Paragraph("4.1 Authentication & Authorization Module", h2))

    story.append(Paragraph("<b>FR-AUTH-01: User Login</b>", h2))
    story.append(Paragraph("• <b>Description:</b> The system shall allow admin, faculty, and students to log in using email/username and password.", bullet))
    story.append(Paragraph("• <b>Input:</b> Email/Username, Password", bullet))
    story.append(Paragraph("• <b>Process:</b> System searches user record and verifies password using bcrypt. Returns a JWT token.", bullet))
    story.append(Paragraph("• <b>Output:</b> JWT access token + user profile data", bullet))
    story.append(Paragraph("• <b>Token Expiry:</b> 24 hours", bullet))
    story.append(Paragraph("• <b>Error Cases:</b> Invalid credentials -> HTTP 400", bullet))

    story.append(Paragraph("<b>FR-AUTH-02: Admin User Creation</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Only authenticated admins can create new user accounts.", bullet))
    story.append(Paragraph("• <b>Input:</b> Full name, email, password, role (student/faculty), degree, year, roll number", bullet))
    story.append(Paragraph("• <b>Process:</b> Admin-authenticated endpoint creates record in User table", bullet))
    story.append(Paragraph("• <b>Validation:</b> Roll number required for students; valid email required", bullet))

    story.append(Paragraph("<b>FR-AUTH-03: Logout</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Users can log out, clearing local storage JWT token.", bullet))
    story.append(Paragraph("• <b>Process:</b> Token removed from client storage; subsequent protected requests rejected.", bullet))

    story.append(Paragraph("<b>FR-AUTH-04: Token Verification</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Protected routes verify the Bearer token before proceeding.", bullet))
    story.append(Paragraph("• <b>Process:</b> JWT decoded -> user looked up by ID -> user attached to req.user", bullet))

    story.append(Paragraph("<b>FR-AUTH-05: Password Change</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Students and Faculty can change their own passwords.", bullet))
    story.append(Paragraph("• <b>Input:</b> Current password, new password (min 6 characters)", bullet))
    story.append(Paragraph("• <b>Process:</b> Verify current password -> bcrypt hash new password -> save", bullet))
    story.append(PageBreak())

    # Page 8: 4.2 Admin Dashboard Module (Screenshot 8)
    story.append(Paragraph("4.2 Admin Dashboard Module", h1))
    story.append(Paragraph("<b>FR-ADMIN-01: Dashboard Overview</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin home page displays aggregated stats:", bullet))
    story.append(Paragraph("  - Total Elections", bullet))
    story.append(Paragraph("  - Active Elections", bullet))
    story.append(Paragraph("  - Total Registered Voters", bullet))
    story.append(Paragraph("  - Total Blockchain Votes Mined", bullet))
    story.append(Paragraph("  - Blockchain Health Status", bullet))
    story.append(Paragraph("• <b>Data Source:</b> <font name='Courier'>GET /api/v1/admin/metrics</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-02: Election Management</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can create, edit, activate, schedule, and close elections.", bullet))
    story.append(Paragraph("• <b>Operations:</b> List all elections; create new election; update status", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/elections, PUT /api/v1/elections/:id/status</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-03: Candidate Management</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can register candidates for an election with full metadata.", bullet))
    story.append(Paragraph("• <b>Fields:</b> Candidate Name, Party / Organization, Manifesto Description, Avatar URL", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/elections/:id/candidates</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-04: Bulk Student Enrollment</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can upload a CSV file to bulk-create student voter accounts.", bullet))
    story.append(Paragraph("• <b>CSV Fields:</b> Full Name, Email, Password, Roll No, Degree, Year", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/admin/import-voters-csv</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-05: Immutable Audit Logs</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can view and download immutable audit logs of all user activities.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/admin/audit-logs</font>", bullet))
    story.append(PageBreak())

    # Page 9-11: 4.3 Student & Faculty & Blockchain Modules (Screenshots 9-11)
    story.append(Paragraph("4.3 Student Dashboard Module (Degree College)", h1))
    story.append(Paragraph("<b>FR-STUDENT-01: Student Home / Active Elections</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Student home page displays greeting, active elections list, and candidate profiles.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/elections</font>", bullet))

    story.append(Paragraph("<b>FR-STUDENT-02: 1-Click Encrypted Voting</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Student selects candidate and casts vote encrypted with AES-256 GCM and signed with ECDSA key pair.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/votes/cast</font>", bullet))

    story.append(Paragraph("<b>FR-STUDENT-03: Anti-Double Voting</b>", h2))
    story.append(Paragraph("• <b>Description:</b> System blocks duplicate vote attempts for the same election and logs violation to audit trail.", bullet))

    story.append(Paragraph("<b>FR-STUDENT-04: Downloadable QR Receipt</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Generates printable QR receipt containing receipt hash, block index, and transaction hash.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/votes/my-receipts</font>", bullet))

    story.append(Paragraph("<b>FR-STUDENT-05: Receipt Verification</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Students can verify any receipt hash against the public blockchain ledger.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/votes/verify-receipt/:hash</font>", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("4.4 Custom Blockchain & AI Module", h1))
    story.append(Paragraph("<b>FR-BLOCKCHAIN-01: Proof-of-Work Block Mining</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Automatically packages queued transactions into blocks meeting SHA-256 difficulty targets.", bullet))

    story.append(Paragraph("<b>FR-BLOCKCHAIN-02: Merkle Tree Generation</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Computes cryptographic binary Merkle Root hash from transaction hashes.", bullet))

    story.append(Paragraph("<b>FR-BLOCKCHAIN-03: Ledger Explorer & Tamper Audit</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Public explorer endpoint allowing block browsing and 1-click full chain validation.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/blockchain/blocks, GET /api/v1/blockchain/verify-chain</font>", bullet))

    story.append(Paragraph("<b>FR-AI-01: AI Fraud Radar & Velocity Analysis</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Analyzes vote velocity bursts (<2s), duplicate IP clusters, and double voting to output threat score (0-100%).", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/ai/fraud-analysis/:election_id</font>", bullet))
    story.append(PageBreak())

    # Page 12: 5. Non-Functional Requirements - Performance (Screenshot 12)
    story.append(Paragraph("5. Non-Functional Requirements", h1))
    story.append(Paragraph("5.1 Performance", h2))
    nfr_perf_data = [
        [Paragraph("Metric", th), Paragraph("Requirement", th)],
        [Paragraph("API Response Time", td), Paragraph("< 2 seconds for standard data endpoints under normal load", td)],
        [Paragraph("File Upload", td), Paragraph("Handles CSV files up to 10 MB; uploads complete within 30 seconds", td)],
        [Paragraph("Block Mining", td), Paragraph("PoW block mined and synced to database within 2 seconds", td)],
        [Paragraph("Concurrent Users", td), Paragraph("Must support at least 100 concurrent users (student project scale)", td)],
    ]
    t_nfr_p = Table(nfr_perf_data, colWidths=[150, 350])
    t_nfr_p.setStyle(ref_table_style)
    story.append(t_nfr_p)
    story.append(Spacer(1, 10))

    # Page 13: 5.2 Security & 5.3 Reliability (Screenshot 13)
    story.append(Paragraph("5.2 Security", h2))
    sec_data = [
        [Paragraph("Requirement", th), Paragraph("Detail", th)],
        [Paragraph("Authentication", td), Paragraph("JWT Bearer tokens, 24-hour expiry", td)],
        [Paragraph("Password Storage", td), Paragraph("bcrypt with salt rounds = 10", td)],
        [Paragraph("Token Blacklisting", td), Paragraph("Logged-out tokens are blacklisted in memory", td)],
        [Paragraph("Rate Limiting", td), Paragraph("Auth routes: strict limiter; Upload routes: upload limiter", td)],
        [Paragraph("CORS", td), Paragraph("Whitelist-only: localhost:3000 and the Vercel production URL", td)],
        [Paragraph("Input Validation", td), Paragraph("Pydantic schemas for all incoming request data", td)],
        [Paragraph("File Security", td), Paragraph("MIME type validation; directory traversal prevention", td)],
        [Paragraph("Vote Encryption", td), Paragraph("AES-256 GCM symmetric vote payload encryption", td)],
        [Paragraph("Transaction Signing", td), Paragraph("ECDSA SECP256R1 asymmetric digital signatures", td)],
    ]
    t_sec = Table(sec_data, colWidths=[150, 350])
    t_sec.setStyle(ref_table_style)
    story.append(t_sec)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.3 Reliability", h2))
    story.append(Paragraph("• System should maintain <b>99% uptime</b> during academic hours (dependent on Vercel and cloud SLAs)", bullet))
    story.append(Paragraph("• All database queries include indexed fields to prevent full collection scans", bullet))

    story.append(Paragraph("5.4 Usability", h2))
    story.append(Paragraph("• Responsive design using Tailwind CSS — supports desktop, tablet, and mobile viewports", bullet))
    story.append(Paragraph("• Framer Motion animations for smooth page transitions and micro-interactions", bullet))
    story.append(Paragraph("• Consistent sidebar-based navigation for all dashboard roles", bullet))

    story.append(Paragraph("5.5 Scalability", h2))
    story.append(Paragraph("• Relational database allows horizontal scaling if the student count grows", bullet))
    story.append(Paragraph("• Stateless JWT authentication design allows multiple backend instances", bullet))

    story.append(Paragraph("5.6 Maintainability", h2))
    story.append(Paragraph("• Clear separation of concerns: routes -> services -> models -> blockchain engine", bullet))
    story.append(PageBreak())

    # Page 14: 6. System Constraints & 7. External Interfaces (Screenshot 14)
    story.append(Paragraph("6. System Constraints", h1))
    story.append(Paragraph("22. Blockchain PoW difficulty target is set to 2 leading zeros for lightweight student project execution.", bullet))
    story.append(Paragraph("23. File Uploads are stored on server local directory — not cloud storage (a limitation for scalability).", bullet))
    story.append(Paragraph("24. Token Blacklist is stored in memory, meaning it resets on server restart.", bullet))
    story.append(Paragraph("25. Vote attempts are limited to one per student per election, enforced by unique compound database constraints.", bullet))
    story.append(Paragraph("26. Admin Password Changes must be done by re-creating the account (no self-service for admins).", bullet))
    story.append(Paragraph("27. The system assumes stable internet connectivity for real-time WebSocket updates.", bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("7. External Interface Requirements", h1))
    story.append(Paragraph("7.1 User Interfaces", h2))
    ui_data = [
        [Paragraph("Page", th), Paragraph("Role", th), Paragraph("Description", th)],
        [Paragraph("Home / Landing Page", td), Paragraph("Public", td), Paragraph("College landing page with login options", td)],
        [Paragraph("Admin Login", td), Paragraph("Admin", td), Paragraph("Separate login page for admin accounts", td)],
        [Paragraph("Student/Faculty Login", td), Paragraph("Student, Faculty", td), Paragraph("Shared login page with role selection", td)],
        [Paragraph("Admin Dashboard", td), Paragraph("Admin", td), Paragraph("Sidebar with Home, Elections, Candidates, Bulk Enrollment, Audit", td)],
        [Paragraph("Student Dashboard", td), Paragraph("Student", td), Paragraph("Sidebar with Home, Elections, Candidates, Vote, Receipts, Verification", td)],
        [Paragraph("Faculty Dashboard", td), Paragraph("Faculty", td), Paragraph("Sidebar with Home, Live Results, Explorer, AI Fraud Radar, Settings", td)],
        [Paragraph("Settings", td), Paragraph("Student, Faculty", td), Paragraph("Password change form", td)],
    ]
    t_ui = Table(ui_data, colWidths=[120, 80, 300])
    t_ui.setStyle(ref_table_style)
    story.append(t_ui)
    story.append(PageBreak())

    # Page 15: 7.2 - 8.1 Data Entities (Screenshot 15)
    story.append(Paragraph("7.2 Hardware Interfaces", h2))
    story.append(Paragraph("• No special hardware required; standard computer, tablet, or smartphone with internet access", bullet))

    story.append(Paragraph("7.3 Software Interfaces", h2))
    sw_data = [
        [Paragraph("System", th), Paragraph("Interface", th)],
        [Paragraph("SQLite / PostgreSQL", td), Paragraph("SQLAlchemy ORM connection protocol", td)],
        [Paragraph("FastAPI WebSockets", td), Paragraph("Real-time bidirectional event manager", td)],
        [Paragraph("Vercel", td), Paragraph("Static hosting via Vercel deployment pipeline", td)],
    ]
    t_sw = Table(sw_data, colWidths=[150, 350])
    t_sw.setStyle(ref_table_style)
    story.append(t_sw)

    story.append(Spacer(1, 10))
    story.append(Paragraph("7.4 Communication Interfaces", h2))
    story.append(Paragraph("• <b>Protocol:</b> HTTPS (production), HTTP (local development)", bullet))
    story.append(Paragraph("• <b>Data Format:</b> JSON (REST API)", bullet))
    story.append(Paragraph("• <b>Auth Header:</b> Authorization: Bearer &lt;JWT_TOKEN&gt;", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Data Requirements", h1))
    story.append(Paragraph("8.1 Data Entities (Degree College Specific)", h2))
    de_data = [
        [Paragraph("Entity", th), Paragraph("Collection / Table", th), Paragraph("Key Fields", th)],
        [Paragraph("Admin", td), Paragraph("users", td), Paragraph("fullName, email, password (hashed), role='admin'", td)],
        [Paragraph("DC Student", td), Paragraph("users", td), Paragraph("fullName, email, password, rollNo, degree, year, semester, class, role='voter'", td)],
        [Paragraph("DC Faculty", td), Paragraph("users", td), Paragraph("fullName, email, password, subject, course, role='observer'", td)],
        [Paragraph("Election", td), Paragraph("elections", td), Paragraph("title, description, status, start_time, end_time, created_by", td)],
        [Paragraph("Candidate", td), Paragraph("candidates", td), Paragraph("election_id, name, party, manifesto, avatar_url, vote_count", td)],
        [Paragraph("Vote", td), Paragraph("votes", td), Paragraph("user_id, election_id, candidate_id, voter_hash, tx_hash, block_index, receipt_hash", td)],
        [Paragraph("Block", td), Paragraph("blocks", td), Paragraph("index, timestamp, previous_hash, hash, nonce, merkle_root, signature", td)],
        [Paragraph("Transaction", td), Paragraph("transactions", td), Paragraph("tx_hash, block_index, election_id, voter_hash, encrypted_vote, signature", td)],
        [Paragraph("Audit Log", td), Paragraph("audit_logs", td), Paragraph("user_id, user_email, action, details, ip_address, timestamp", td)],
    ]
    t_de = Table(de_data, colWidths=[90, 90, 320])
    t_de.setStyle(ref_table_style)
    story.append(t_de)
    story.append(PageBreak())

    # Page 16: 8.2 Retention & 8.3 Integrity (Screenshot 16)
    story.append(Paragraph("8.2 Data Retention", h1))
    story.append(Paragraph("• Student audit and activity logs are timestamped and indexed; no automatic purging defined", bullet))
    story.append(Paragraph("• Blockchain blocks and vote transactions are immutable — once mined, records persist permanently", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8.3 Data Integrity", h1))
    story.append(Paragraph("• Unique email and username constraints on User collection", bullet))
    story.append(Paragraph("• Unique compound constraint on Vote (user_id, election_id) — one vote per student per election", bullet))
    story.append(Paragraph("• Unique index on Block (index, hash) and Transaction (tx_hash) to guarantee ledger uniqueness", bullet))
    story.append(PageBreak())

    # =========================================================================
    # ========================== PART 2: UML ==================================
    # =========================================================================

    # Page 18: UML Cover (Screenshot 18)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>UML</b>", cover_style))
    story.append(PageBreak())

    # Page 19: UML Diagrams Complete Set (Screenshot 19)
    story.append(Paragraph("UML Diagrams — Complete Set", doc_header))
    story.append(Spacer(1, 10))
    story.append(Paragraph("TRCAC Blockchain Voting System — Degree College Module", doc_main_title))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Table of Contents</b>", doc_title))
    uml_toc_items = [
        "1. &nbsp;Use Case Diagram",
        "2. &nbsp;Class Diagram",
        "3. &nbsp;Sequence Diagram — Login Flow",
        "4. &nbsp;Sequence Diagram — Encrypted Vote & Block Mining",
        "5. &nbsp;Sequence Diagram — Receipt Verification Flow",
        "6. &nbsp;Activity Diagram — AI Fraud Detection & Velocity Marking",
        "7. &nbsp;Component Diagram",
        "8. &nbsp;ER Diagram (Database)"
    ]
    for item in uml_toc_items:
        story.append(Paragraph(item, bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("1. Use Case Diagram", h1))
    story.append(Paragraph("Each role is shown in a separate diagram for A4 readability.", body))
    story.append(Paragraph("1.1 Admin Use Cases", h2))
    story.append(Paragraph("Admin -> [Login / Logout, Create Student Account, Create Faculty Account, Manage Elections, Manage Candidates, Bulk Enroll Students, Bulk Add Candidates, View Dashboard Stats, View & Delete Users, View Audit Logs]", bullet))
    story.append(PageBreak())

    # Page 21-22: 1.2 DC Faculty & 1.3 DC Student Use Cases (Screenshots 21-22)
    story.append(Paragraph("1.2 DC Faculty / Observer Use Cases", h1))
    story.append(Paragraph("DC Faculty -> [Login / Logout, Change Password, View Dashboard, View Live Standings, View Block Explorer, Audit Chain Integrity, View AI Fraud Alerts, Download Reports]", bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("1.3 DC Student / Voter Use Cases", h1))
    story.append(Paragraph("DC Student -> [Login / Logout, Change Password, View Dashboard, View Active Elections, View Candidate Profiles, Cast Encrypted Vote, Download QR Receipt, Verify Receipt Hash]", bullet))
    story.append(PageBreak())

    # Page 23-25: 2. Class Diagram Groups (Screenshots 23-25)
    story.append(Paragraph("2. Class Diagram", h1))
    story.append(Paragraph("Split into three focused groups for clarity on A4.", body))
    story.append(Paragraph("2.1 User & Auth Classes", h2))
    story.append(Paragraph("<b>User Base Class:</b> +id, +fullName, +email, +password, +role, +lastLogin | +login()<br/>"
                           "<b>extends DCStudent:</b> +rollNo, +degree, +year, +semester, +class, +college | +changePassword()<br/>"
                           "<b>extends DCFaculty:</b> +subject, +courses[], +teachingAssignments[], +college | +changePassword()", body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.2 Content & Progress Classes", h2))
    story.append(Paragraph("<b>Election Class:</b> +id, +title, +description, +status, +startTime, +endTime<br/>"
                           "<b>Candidate Class:</b> +id, +electionId, +name, +party, +manifesto, +voteCount<br/>"
                           "<b>Block Class:</b> +index, +timestamp, +previousHash, +hash, +nonce, +merkleRoot, +signature | +calculateHash()", body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 Assessment & Activity Classes", h2))
    story.append(Paragraph("<b>Vote Class:</b> +id, +userId, +electionId, +candidateId, +voterHash, +encryptedVote, +txHash, +receiptHash<br/>"
                           "<b>AuditLog Class:</b> +id, +userId, +userEmail, +action, +details, +ipAddress, +timestamp", body))
    story.append(PageBreak())

    # Page 26-28: Sequence Diagrams (Screenshots 26-28)
    story.append(Paragraph("3. Sequence Diagram — Login Flow", h1))
    story.append(Paragraph("Student -> React Frontend -> POST /api/v1/auth/login -> FastAPI -> Search User by email -> bcrypt verify password -> Generate JWT Token (24h) -> Return 200 {token, user} -> Save to storage -> Redirect to Dashboard.", body))

    story.append(Spacer(1, 15))
    story.append(Paragraph("4. Sequence Diagram — Encrypted Vote & Block Mining", h1))
    story.append(Paragraph("Student -> Select Candidate -> Click Vote -> AES-256 GCM Encrypt -> ECDSA Sign -> POST /api/v1/votes/cast -> FastAPI -> Check single-vote rule -> Queue Transaction -> Mine PoW Block (calculate Merkle Root) -> Save Vote to DB -> Broadcast WebSockets -> Return QR Receipt.", body))

    story.append(Spacer(1, 15))
    story.append(Paragraph("5. Sequence Diagram — Receipt Verification Flow", h1))
    story.append(Paragraph("Student / Auditor -> Enter Receipt Hash -> GET /api/v1/votes/verify-receipt/:hash -> FastAPI -> Lookup Vote by receipt_hash -> Search Blockchain Ledger for tx_hash -> Verify block index -> Return {verified: True, block_index, tx_hash, voter_hash}.", body))
    story.append(PageBreak())

    # Page 29-30: Activity Diagram & Component Diagram (Screenshots 29-30)
    story.append(Paragraph("6. Activity Diagram — AI Fraud Detection & Velocity Marking", h1))
    story.append(Paragraph("Start -> Vote Submitted -> Read Timestamp & Client IP -> Compute Delta Time between consecutive votes -> Delta < 2.0s? -> Yes: Flag High Velocity Anomaly -> Count IP submissions > 5? -> Yes: Flag IP Concentration -> Double-Vote attempts detected? -> Yes: Add Double-Vote Penalty -> Calculate Unified Fraud Risk Score (0-100%) -> Output Risk Level (Low/Medium/High/Critical) -> End.", body))

    story.append(Spacer(1, 15))
    story.append(Paragraph("7. Component Diagram", h1))
    story.append(Paragraph("7.1 Frontend Components (React SPA: AuthContext, Sidebar, AdminDashboard, VoterDashboard, ObserverDashboard, Explorer)", body))
    story.append(Paragraph("7.2 Backend Components (FastAPI Router: auth.py, elections.py, votes.py, blockchain.py, admin.py, ai.py, observer.py)", body))
    story.append(Paragraph("7.3 Full System Overview (Browser -> HTTPS/WSS -> FastAPI ASGI Server -> Blockchain Engine + SQLite/PostgreSQL Database)", body))

    story.append(Spacer(1, 15))
    story.append(Paragraph("8. Entity-Relationship (ER) Diagram", h1))
    story.append(Paragraph("8.1 Core User & Content Entities: users (1:N) elections, elections (1:N) candidates", body))
    story.append(Paragraph("8.2 Voting & Ledger Entities: users (1:N) votes, elections (1:N) votes, blocks (1:N) transactions", body))
    story.append(PageBreak())

    # =========================================================================
    # ========================== PART 3: ADD ==================================
    # =========================================================================

    # Page 33: ADD Cover (Screenshot 33)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>ADD</b>", cover_style))
    story.append(PageBreak())

    # Page 34: ADD Title, Scope, 1. Introduction & Goals (Screenshot 34)
    story.append(Paragraph("Architecture Design Document (ADD)", doc_header))
    story.append(Spacer(1, 10))
    story.append(Paragraph("TRCAC Blockchain Voting System — Degree College Module", doc_main_title))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Version: 1.0 | Date: July 2026 | Scope: Degree College Only", doc_subtitle))
    story.append(Spacer(1, 15))

    story.append(Paragraph("1. Introduction & Goals", h1))
    story.append(Paragraph(
        "This document describes the structural design of the TRCAC BVS Degree College Module — "
        "how it is organised, why key decisions were made, and how all parts connect.",
        body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Architectural Goals", h2))

    goals_data = [
        [Paragraph("Goal", th), Paragraph("Description", th)],
        [Paragraph("Separation of Concerns", td), Paragraph("UI never touches database directly — frontend and backend are fully separate", td)],
        [Paragraph("Role-Based Security", td), Paragraph("Every protected route enforces Admin / Faculty / Student role checks", td)],
        [Paragraph("Stateless Auth", td), Paragraph("JWT-based authentication allows multiple backend instances without shared sessions", td)],
        [Paragraph("Simplicity", td), Paragraph("Clean architecture — Python 3.12 FastAPI backend + React 19 frontend", td)],
        [Paragraph("Maintainability", td), Paragraph("Modular clean code, environment variables, and clear directory structure throughout", td)],
    ]
    t_goals = Table(goals_data, colWidths=[140, 360])
    t_goals.setStyle(ref_table_style)
    story.append(t_goals)
    story.append(PageBreak())

    # Page 35: 2. System Context, 2.1 Actors and External Systems (Screenshot 35)
    story.append(Paragraph("2. System Context", h1))
    story.append(Paragraph("2.1 Actors and External Systems", h2))

    sys_data = [
        [Paragraph("Actor / System", th), Paragraph("Type", th), Paragraph("Role", th)],
        [Paragraph("Admin", td), Paragraph("User", td), Paragraph("Creates accounts, manages elections/candidates, bulk ops", td)],
        [Paragraph("DC Faculty", td), Paragraph("User", td), Paragraph("Monitors live results, audits ledger, checks AI fraud radar", td)],
        [Paragraph("DC Student", td), Paragraph("User", td), Paragraph("Casts encrypted votes, generates receipts, verifies hashes", td)],
        [Paragraph("SQLite / PostgreSQL", td), Paragraph("External Service", td), Paragraph("Cloud-hosted / local relational database", td)],
        [Paragraph("Custom Blockchain", td), Paragraph("Core Engine", td), Paragraph("Hosts and mines immutable SHA-256 block ledger", td)],
        [Paragraph("Vercel", td), Paragraph("External Service", td), Paragraph("Hosts and serves the React frontend (CDN)", td)],
    ]
    t_sys = Table(sys_data, colWidths=[120, 90, 290])
    t_sys.setStyle(ref_table_style)
    story.append(t_sys)
    story.append(Spacer(1, 15))

    # Page 36: 3. Overall Architecture — Three-Tier Model (Screenshot 36)
    story.append(Paragraph("3. Overall Architecture — Three-Tier Model", h1))
    story.append(Paragraph("3.1 Architecture Layers", h2))
    story.append(Paragraph("• <b>Tier 1 — Presentation:</b> Browser -> React + Vite + Tailwind CSS Single Page Application", bullet))
    story.append(Paragraph("• <b>Tier 2 — Application:</b> FastAPI REST API (Auth Middleware, AI Fraud Radar, WebSockets)", bullet))
    story.append(Paragraph("• <b>Tier 3 — Data & Ledger:</b> Custom Python SHA-256 Blockchain Engine + SQLite/PostgreSQL Database", bullet))
    story.append(PageBreak())

    # Page 37: 4. Frontend Architecture, 4.1 Tech Stack, 4.2 Routing Structure (Screenshot 37)
    story.append(Paragraph("4. Frontend Architecture", h1))
    story.append(Paragraph("4.1 Technology Stack", h2))

    fe_data = [
        [Paragraph("Technology", th), Paragraph("Version", th), Paragraph("Role", th)],
        [Paragraph("React", td), Paragraph("19.0", td), Paragraph("UI library", td)],
        [Paragraph("Vite", td), Paragraph("5.x / 7.x", td), Paragraph("Build tool + HMR dev server", td)],
        [Paragraph("React Router DOM", td), Paragraph("6.x", td), Paragraph("Client-side routing", td)],
        [Paragraph("Tailwind CSS", td), Paragraph("3.4", td), Paragraph("Utility-first styling & Dark Mode", td)],
        [Paragraph("Framer Motion", td), Paragraph("11.x", td), Paragraph("Page transitions and animations", td)],
        [Paragraph("Axios", td), Paragraph("1.x", td), Paragraph("HTTP client for API calls", td)],
        [Paragraph("Recharts", td), Paragraph("2.x", td), Paragraph("Live vote distribution charts", td)],
    ]
    t_fe = Table(fe_data, colWidths=[130, 80, 290])
    t_fe.setStyle(ref_table_style)
    story.append(t_fe)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.2 Routing Structure", h2))
    story.append(Paragraph("• <font name='Courier'>/login</font> -> Shared login page with role detection", bullet))
    story.append(Paragraph("• <font name='Courier'>/admin</font> -> Protected Admin Dashboard (Overview, Elections, Candidates, Import)", bullet))
    story.append(Paragraph("• <font name='Courier'>/voter</font> -> Protected Voter Dashboard (Active Ballots, Cast Vote, QR Receipt)", bullet))
    story.append(Paragraph("• <font name='Courier'>/observer</font> -> Protected Faculty / Observer Live Standings", bullet))
    story.append(Paragraph("• <font name='Courier'>/explorer</font> -> Public Blockchain Ledger Browser", bullet))
    story.append(PageBreak())

    # Page 38: 5. Backend Architecture, 5.1 Tech Stack (Screenshot 38)
    story.append(Paragraph("5. Backend Architecture", h1))
    story.append(Paragraph("5.1 Technology Stack", h2))

    be_data = [
        [Paragraph("Technology", th), Paragraph("Version", th), Paragraph("Role", th)],
        [Paragraph("Python", td), Paragraph("3.12+", td), Paragraph("Server runtime", td)],
        [Paragraph("FastAPI", td), Paragraph("0.111+", td), Paragraph("Web framework", td)],
        [Paragraph("SQLAlchemy", td), Paragraph("2.0+", td), Paragraph("Database ORM", td)],
        [Paragraph("PyJWT", td), Paragraph("2.8+", td), Paragraph("JWT auth tokens", td)],
        [Paragraph("bcrypt", td), Paragraph("4.1+", td), Paragraph("Password hashing", td)],
        [Paragraph("Cryptography", td), Paragraph("42.0+", td), Paragraph("ECDSA SECP256R1 & AES-256 GCM algorithms", td)],
        [Paragraph("WebSockets", td), Paragraph("12.0+", td), Paragraph("Real-time push event manager", td)],
    ]
    t_be = Table(be_data, colWidths=[130, 80, 290])
    t_be.setStyle(ref_table_style)
    story.append(t_be)
    story.append(Spacer(1, 15))

    # Page 39: 5.3 Rate Limiting Strategy & 5.4 API Route Map (Screenshot 39)
    story.append(Paragraph("5.3 Rate Limiting Strategy", h1))
    rl_data = [
        [Paragraph("Route Group", th), Paragraph("Limiter Type", th), Paragraph("Reason", th)],
        [Paragraph("/api/v1/auth", td), Paragraph("Strict (auth limiter)", td), Paragraph("Block brute-force login", td)],
        [Paragraph("/api/v1/votes", td), Paragraph("Vote limiter", td), Paragraph("Prevent automated double-vote bursts", td)],
        [Paragraph("/api/v1/admin", td), Paragraph("Upload limiter", td), Paragraph("Prevent file upload abuse", td)],
        [Paragraph("All others", td), Paragraph("General limiter", td), Paragraph("General DDoS protection", td)],
    ]
    t_rl = Table(rl_data, colWidths=[120, 130, 250])
    t_rl.setStyle(ref_table_style)
    story.append(t_rl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.4 API Route Map", h2))
    route_map = [
        [Paragraph("Prefix", th), Paragraph("File", th), Paragraph("Key Endpoints", th)],
        [Paragraph("/api/v1/auth", td), Paragraph("auth.py", td), Paragraph("login, register, me", td)],
        [Paragraph("/api/v1/elections", td), Paragraph("elections.py", td), Paragraph("create, list, status, add candidate", td)],
        [Paragraph("/api/v1/votes", td), Paragraph("votes.py", td), Paragraph("cast, my-receipts, verify-receipt", td)],
        [Paragraph("/api/v1/blockchain", td), Paragraph("blockchain.py", td), Paragraph("blocks, search, status, verify-chain", td)],
        [Paragraph("/api/v1/admin", td), Paragraph("admin.py", td), Paragraph("metrics, import-voters-csv, audit-logs", td)],
        [Paragraph("/api/v1/ai", td), Paragraph("ai.py", td), Paragraph("fraud-analysis", td)],
        [Paragraph("/api/v1/observer", td), Paragraph("observer.py", td), Paragraph("live-results", td)],
    ]
    t_rm = Table(route_map, colWidths=[110, 90, 300])
    t_rm.setStyle(ref_table_style)
    story.append(t_rm)
    story.append(PageBreak())

    # Page 40: 6. Database Architecture, 6.1 Collections Summary (Screenshot 40)
    story.append(Paragraph("6. Database Architecture", h1))
    story.append(Paragraph("6.1 Collections / Tables Summary (DC Scope)", h2))

    col_data = [
        [Paragraph("Collection / Table", th), Paragraph("Model", th), Paragraph("Purpose", th)],
        [Paragraph("users", td), Paragraph("User", td), Paragraph("Admin, student, and faculty accounts", td)],
        [Paragraph("elections", td), Paragraph("Election", td), Paragraph("Election metadata and lifecycle state", td)],
        [Paragraph("candidates", td), Paragraph("Candidate", td), Paragraph("Candidate nominations and tallies", td)],
        [Paragraph("votes", td), Paragraph("Vote", td), Paragraph("Encrypted vote records and receipts", td)],
        [Paragraph("blocks", td), Paragraph("BlockModel", td), Paragraph("Mined blockchain block headers", td)],
        [Paragraph("transactions", td), Paragraph("TransactionModel", td), Paragraph("Encrypted ledger transactions", td)],
        [Paragraph("audit_logs", td), Paragraph("AuditLog", td), Paragraph("Immutable security action logs", td)],
    ]
    t_col = Table(col_data, colWidths=[120, 100, 280])
    t_col.setStyle(ref_table_style)
    story.append(t_col)
    story.append(Spacer(1, 10))

    # Page 41: 6.2 Key Indexes (Screenshot 41)
    story.append(Paragraph("6.2 Key Indexes", h2))
    idx_data = [
        [Paragraph("Collection / Table", th), Paragraph("Index", th), Paragraph("Type", th)],
        [Paragraph("users", td), Paragraph("email, username", td), Paragraph("Unique", td)],
        [Paragraph("votes", td), Paragraph("(user_id, election_id)", td), Paragraph("Unique Compound", td)],
        [Paragraph("votes", td), Paragraph("tx_hash, receipt_hash", td), Paragraph("Unique", td)],
        [Paragraph("blocks", td), Paragraph("index, hash", td), Paragraph("Unique", td)],
        [Paragraph("transactions", td), Paragraph("tx_hash", td), Paragraph("Unique", td)],
        [Paragraph("audit_logs", td), Paragraph("(user_id, timestamp)", td), Paragraph("Compound", td)],
    ]
    t_idx = Table(idx_data, colWidths=[130, 150, 220])
    t_idx.setStyle(ref_table_style)
    story.append(t_idx)
    story.append(PageBreak())

    # Page 42-43: 6.3 Class Name Convention & 7. Authentication Architecture (Screenshots 42-43)
    story.append(Paragraph("6.3 Degree College Class Name Convention", h1))
    class_conv_data = [
        [Paragraph("Degree", th), Paragraph("Code", th), Paragraph("FY", th), Paragraph("SY", th), Paragraph("TY", th)],
        [Paragraph("B.Sc (CS)", td), Paragraph("BScCS", td), Paragraph("FYBScCS", td), Paragraph("SYBScCS", td), Paragraph("TYBScCS", td)],
        [Paragraph("B.Sc (IT)", td), Paragraph("BScIT", td), Paragraph("FYBScIT", td), Paragraph("SYBScIT", td), Paragraph("TYBScIT", td)],
        [Paragraph("BA", td), Paragraph("BA", td), Paragraph("FYBA", td), Paragraph("SYBA", td), Paragraph("TYBA", td)],
        [Paragraph("BMS", td), Paragraph("BMS", td), Paragraph("FYBMS", td), Paragraph("SYBMS", td), Paragraph("TYBMS", td)],
        [Paragraph("BCom", td), Paragraph("BCom", td), Paragraph("FYBCom", td), Paragraph("SYBCom", td), Paragraph("TYBCom", td)],
        [Paragraph("BAF", td), Paragraph("BAF", td), Paragraph("FYBAF", td), Paragraph("SYBAF", td), Paragraph("TYBAF", td)],
        [Paragraph("BAMMC", td), Paragraph("BAMMC", td), Paragraph("FYBAMMC", td), Paragraph("SYBAMMC", td), Paragraph("TYBAMMC", td)],
    ]
    t_cc = Table(class_conv_data, colWidths=[100, 70, 110, 110, 110])
    t_cc.setStyle(ref_table_style)
    story.append(t_cc)
    story.append(Spacer(1, 15))

    story.append(Paragraph("7. Authentication & Authorization Architecture", h1))
    story.append(Paragraph("7.1 JWT Token Structure", h2))

    jwt_data = [
        [Paragraph("Field", th), Paragraph("Value", th)],
        [Paragraph("Algorithm", td), Paragraph("HS256", td)],
        [Paragraph("sub (userId)", td), Paragraph("Database integer ID of user", td)],
        [Paragraph("role", td), Paragraph("student / faculty / admin", td)],
        [Paragraph("email", td), Paragraph("User registered institutional email address", td)],
        [Paragraph("exp", td), Paragraph("Issued at + 24 hours", td)],
    ]
    t_jwt = Table(jwt_data, colWidths=[130, 370])
    t_jwt.setStyle(ref_table_style)
    story.append(t_jwt)
    story.append(PageBreak())

    # Page 51: 9.2 Security Measures Summary (Screenshot 51)
    story.append(Paragraph("9. Security Architecture", h1))
    story.append(Paragraph("9.2 Security Measures Summary", h2))

    sec_summary_data = [
        [Paragraph("Threat", th), Paragraph("Countermeasure", th), Paragraph("Implementation", th)],
        [Paragraph("Brute force login", td), Paragraph("Strict rate limiter", td), Paragraph("Rate limiting middleware on /api/v1/auth", td)],
        [Paragraph("Token reuse after logout", td), Paragraph("Token blacklist / localStorage wipe", td), Paragraph("Client-side storage wipe + server blacklist", td)],
        [Paragraph("Password cracking", td), Paragraph("bcrypt hashing", td), Paragraph("10 salt rounds with salted hashes", td)],
        [Paragraph("Cross-origin requests", td), Paragraph("CORS whitelist", td), Paragraph("Only frontend origin URL allowed", td)],
        [Paragraph("Clickjacking", td), Paragraph("X-Frame-Options: DENY", td), Paragraph("FastAPI security headers middleware", td)],
        [Paragraph("Vote choice exposure", td), Paragraph("AES-256 GCM encryption", td), Paragraph("Vote payload encrypted with 32-byte secret key", td)],
        [Paragraph("Transaction forgery", td), Paragraph("ECDSA SECP256R1 signatures", td), Paragraph("Digital signatures verified before block mining", td)],
        [Paragraph("SQL Injection", td), Paragraph("SQLAlchemy ORM parameterized queries", td), Paragraph("Zero raw string SQL concatenation", td)],
        [Paragraph("Secret leakage", td), Paragraph("dotenv + .gitignore", td), Paragraph("SECRET_KEY, DATABASE_URL in .env file", td)],
    ]
    t_sec_sum = Table(sec_summary_data, colWidths=[120, 150, 230])
    t_sec_sum.setStyle(ref_table_style)
    story.append(t_sec_sum)
    story.append(Spacer(1, 15))

    # Page 52: 10. Deployment Architecture & 10.2 Environment Variables (Screenshot 52)
    story.append(Paragraph("10. Deployment Architecture", h1))
    story.append(Paragraph("10.2 Environment Variables", h2))

    env_vars_data = [
        [Paragraph("Variable", th), Paragraph("Used In", th), Paragraph("Purpose", th)],
        [Paragraph("DATABASE_URL", td), Paragraph("Backend", td), Paragraph("SQLite / PostgreSQL database connection string", td)],
        [Paragraph("SECRET_KEY", td), Paragraph("Backend", td), Paragraph("JWT signing secret key", td)],
        [Paragraph("VOTE_ENCRYPTION_KEY", td), Paragraph("Backend", td), Paragraph("32-byte AES-256 GCM vote payload key", td)],
        [Paragraph("BLOCKCHAIN_DIFFICULTY", td), Paragraph("Backend", td), Paragraph("Proof-of-Work leading zero difficulty (default 2)", td)],
        [Paragraph("PORT", td), Paragraph("Backend", td), Paragraph("Server port (default 8000)", td)],
    ]
    t_ev = Table(env_vars_data, colWidths=[140, 70, 290])
    t_ev.setStyle(ref_table_style)
    story.append(t_ev)
    story.append(PageBreak())

    # Page 53: 11. Key Design Decisions (Screenshot 53)
    story.append(Paragraph("11. Key Design Decisions", h1))
    decisions_matrix = [
        [Paragraph("#", th), Paragraph("Decision", th), Paragraph("Choice", th), Paragraph("Rationale", th), Paragraph("Tradeoff", th)],
        [Paragraph("1", td), Paragraph("User storage", td), Paragraph("Unified users table with role", td), Paragraph("Unified auth lookup across admin, students, faculty", td), Paragraph("Role check required on protected routes", td)],
        [Paragraph("2", td), Paragraph("Vote Secrecy", td), Paragraph("AES-256 GCM encryption", td), Paragraph("Prevents ballot choice from being public on ledger", td), Paragraph("Server holds symmetric key for decryption", td)],
        [Paragraph("3", td), Paragraph("Voter Auth", td), Paragraph("ECDSA SECP256R1 signatures", td), Paragraph("Digital signatures guarantee vote authenticity", td), Paragraph("Keypair generated per vote transaction", td)],
        [Paragraph("4", td), Paragraph("Real-Time", td), Paragraph("FastAPI WebSockets", td), Paragraph("Instant push broadcasts to live dashboards", td), Paragraph("Active socket connection management", td)],
        [Paragraph("5", td), Paragraph("Threat Radar", td), Paragraph("Heuristic Velocity Analysis", td), Paragraph("Detects bursts (<2s), duplicate IPs, double voting", td), Paragraph("Thresholds require tuning for scale", td)],
        [Paragraph("6", td), Paragraph("Tech stack", td), Paragraph("Python FastAPI + React 19", td), Paragraph("High performance, asynchronous, modern ecosystem", td), Paragraph("Two language environments (Python + TS)", td)],
    ]
    t_dec_m = Table(decisions_matrix, colWidths=[15, 75, 110, 155, 145])
    t_dec_m.setStyle(ref_table_style)
    story.append(t_dec_m)

    # Build PDF Documents
    doc.build(story)
    print(f"Successfully generated Project Report PDF at: {filename}")

    # Also save as All_In_One and SRS for complete coverage
    for extra_file in ["docs/Blockchain_Voting_System_All_In_One_Project_Report.pdf", "docs/Blockchain_Voting_System_SRS.pdf"]:
        doc_extra = SimpleDocTemplate(extra_file, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
        doc_extra.build(story)
        print(f"Successfully generated PDF at: {extra_file}")

if __name__ == "__main__":
    generate_exact_reference_pdf()
