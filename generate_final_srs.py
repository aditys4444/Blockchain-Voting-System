import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def generate_srs_pdf(filename="docs/Blockchain_Voting_System_SRS.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Exact Typography Matching Reference Format
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
        leading=14.5,
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
    # Page 1: Cover Page (Exact match to Reference Page 1)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>SRS</b>", cover_style))
    story.append(PageBreak())

    # =========================================================================
    # Page 2: Title, Metadata, TOC, 1. Introduction, 1.1 Purpose (Reference Page 2)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("Software Requirements Specification (SRS)", doc_header))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Blockchain Voting System (BVS)", doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Cryptographic E-Voting & Decentralized Ledger Module", doc_subtitle))
    story.append(Spacer(1, 15))

    meta_text = """
    <b>Document Version:</b> 1.0<br/>
    <b>Prepared By:</b> Aditya Yadav<br/>
    <b>Department:</b> B.Sc Computer Science<br/>
    <b>Institution:</b> Thakur Ramnarayan College of Arts & Commerce (TRCAC)<br/>
    <b>Academic Year:</b> 2026-2027<br/>
    <b>Date:</b> August 2026<br/>
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
        "<b>Blockchain Voting System (BVS) — Cryptographic E-Voting & Decentralized Ledger Module</b>. It is intended as a reference for the "
        "development team, evaluators, instructors, and any stakeholders involved in reviewing, testing, deploying, or auditing the system.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # Page 3: 1.2 Scope & Election Types Table & User Roles (Reference Page 3)
    # =========================================================================
    story.append(Paragraph("1.2 Scope", h1))
    story.append(Paragraph(
        "The <b>Blockchain Voting System (BVS)</b> is a secure, decentralized web-based platform designed to conduct tamper-evident, "
        "cryptographically verifiable elections across general organizations, academic institutions, and enterprise bodies. "
        "The system supports multiple election domains and configurable voter electorates:",
        body
    ))
    story.append(Spacer(1, 6))

    domain_data = [
        [Paragraph("Election Category", th), Paragraph("Configurable Electorates & Sub-divisions", th)],
        [Paragraph("Institutional / Campus Elections", td), Paragraph("Student Council, Department Representative, Senate, Faculty Committee", td)],
        [Paragraph("Organizational / Corporate Ballots", td), Paragraph("Board of Directors, Shareholder Voting, Executive Committee, Union Elections", td)],
        [Paragraph("Community & Guild Elections", td), Paragraph("Association Leadership, Civic Panels, Club Executives, Regional Delegates", td)],
        [Paragraph("General E-Voting & Polls", td), Paragraph("Multi-candidate Polls, Referendums, Resolution Approvals, Policy Feedback", td)],
        [Paragraph("Academic Departments (TRCAC)", td), Paragraph("B.Sc CS, B.Sc IT, BA, BAMMC, BMS, B.Com, BAF (FY, SY, TY cohorts)", td)],
    ]
    t_domain = Table(domain_data, colWidths=[200, 300])
    t_domain.setStyle(ref_table_style)
    story.append(t_domain)
    story.append(Spacer(1, 10))

    story.append(Paragraph("The system has three primary user roles: <b>Admin</b>, <b>Voter</b>, and <b>Observer / Auditor</b>, each equipped with dedicated dashboards, security boundaries, and authorization privileges.", body))
    story.append(PageBreak())

    # =========================================================================
    # Page 4: 1.3 Definitions & Acronyms, 1.4 References, 1.5 Overview, 2. Overall Description (Reference Page 4)
    # =========================================================================
    story.append(Paragraph("1.3 Definitions & Acronyms", h1))
    terms_data = [
        [Paragraph("Term", th), Paragraph("Definition", th)],
        [Paragraph("BVS", td), Paragraph("Blockchain Voting System", td)],
        [Paragraph("PoW", td), Paragraph("Proof-of-Work consensus algorithm enforcing computational block mining", td)],
        [Paragraph("ECDSA", td), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1 curve)", td)],
        [Paragraph("AES-256 GCM", td), Paragraph("Advanced Encryption Standard (256-bit) with Galois/Counter Mode authenticated encryption", td)],
        [Paragraph("SHA-256", td), Paragraph("Secure Hash Algorithm 256-bit cryptographic digest function", td)],
        [Paragraph("Merkle Tree", td), Paragraph("Cryptographic binary hash tree aggregating all transactions within a block", td)],
        [Paragraph("JWT", td), Paragraph("JSON Web Token — stateless cryptographic bearer token for session authentication", td)],
        [Paragraph("API", td), Paragraph("Application Programming Interface", td)],
        [Paragraph("CRUD", td), Paragraph("Create, Read, Update, Delete", td)],
        [Paragraph("TRCAC", td), Paragraph("Thakur Ramnarayan College of Arts & Commerce", td)],
    ]
    t_terms = Table(terms_data, colWidths=[120, 380])
    t_terms.setStyle(ref_table_style)
    story.append(t_terms)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.4 References", h2))
    story.append(Paragraph("• Project Codebase: blockchain-voting-system (GitHub Repository)", bullet))
    story.append(Paragraph("• NIST Special Publication 800-38D (Recommendation for GCM Block Cipher Mode)", bullet))
    story.append(Paragraph("• SEC 2: Recommended Elliptic Curve Domain Parameters (SECP256R1)", bullet))
    story.append(Paragraph("• System Architecture & Security Specs: SYSTEM_ARCHITECTURE.md", bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("1.5 Overview", h2))
    story.append(Paragraph("The BVS is architected into two decoupled logical tiers:", body))
    story.append(Paragraph("9. &nbsp;<b>Frontend</b> — A responsive React 19 + Vite Single Page Application (SPA) styled with Tailwind CSS", bullet))
    story.append(Paragraph("10. <b>Backend</b> — An asynchronous FastAPI (Python 3.12) REST API connected to database and Custom Blockchain Engine", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Overall Description", h1))
    story.append(Paragraph("2.1 Product Perspective", h2))
    story.append(Paragraph(
        "The Blockchain Voting System is a standalone e-voting solution replacing physical ballot boxes and centralized, opaque databases. "
        "The system can be deployed on local infrastructure or cloud environments.<br/><br/>"
        "The system integrates with:<br/>"
        "• <b>SQLite / PostgreSQL</b> — relational database for relational application metadata<br/>"
        "• <b>Custom Python Blockchain</b> — decentralized SHA-256 ledger engine with Merkle roots<br/>"
        "• <b>FastAPI WebSockets</b> — real-time vote distribution and block broadcast updates",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # Page 5: 2.2 Product Functions, 2.3 User Classes, 2.4 Environment, 2.5 Constraints (Reference Page 5)
    # =========================================================================
    story.append(Paragraph("2.2 Product Functions (High-Level)", h1))
    story.append(Paragraph("The following high-level capabilities are supported by the system:", body))
    high_funcs = [
        "11. User Account Management — Admin creates accounts; role-based login (Admin, Voter, Observer)",
        "12. Election Lifecycle Management — Admin creates, schedules, activates, and closes elections",
        "13. Candidate Nomination Studio — Admin registers candidates with party affiliations and manifestos",
        "14. 1-Click Encrypted Voting — Vote choices encrypted via AES-256 GCM before ledger submission",
        "15. Anti-Double Voting Enforcement — Single vote per registered voter strictly enforced at database and chain level",
        "16. Digital Signature Signing — Transactions signed using single-use voter ECDSA key pairs",
        "17. Proof-of-Work Block Mining — Mined blocks aggregate queued transactions meeting SHA-256 difficulty targets",
        "18. Downloadable QR Receipt — Generates printable receipt containing receipt hash, block index, and tx hash",
        "19. Bulk Voter Enrollment — Admin bulk-enrolls voters via CSV file upload",
        "20. Blockchain Explorer — Public block browser, transaction lookup, and 1-click ledger tamper auditor",
        "21. AI Fraud Radar — Analyzes vote velocity bursts (<2s), duplicate IP clusters, and double-voting threat index"
    ]
    for hf in high_funcs:
        story.append(Paragraph(hf, bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 User Classes", h1))
    uc_data = [
        [Paragraph("User Class", th), Paragraph("Description", th)],
        [Paragraph("Admin", td), Paragraph("Full administrative control. Manages elections, candidate profiles, bulk voter enrollment, and audit logs.", td)],
        [Paragraph("Voter", td), Paragraph("Casts encrypted ballots in active elections, downloads QR receipts, and verifies receipt hashes on the ledger.", td)],
        [Paragraph("Observer / Auditor", td), Paragraph("Read-only transparency access. Watches live Recharts vote tallies, inspects block explorer, verifies chain integrity, and views AI fraud alerts.", td)],
    ]
    t_uc = Table(uc_data, colWidths=[130, 370])
    t_uc.setStyle(ref_table_style)
    story.append(t_uc)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.4 Operating Environment", h1))
    story.append(Paragraph("• <b>Client Side:</b> Modern web browser (Chrome, Firefox, Edge, Safari)", bullet))
    story.append(Paragraph("• <b>Server Side:</b> Python 3.12+, FastAPI 0.111+, Uvicorn 0.30+", bullet))
    story.append(Paragraph("• <b>Database:</b> SQLite (local development) / PostgreSQL (cloud-hosted production)", bullet))
    story.append(Paragraph("• <b>Frontend Build Tool:</b> Vite 5.x / 7.x", bullet))
    story.append(Paragraph("• <b>Deployment:</b> Docker, Docker Compose, or Vercel / Cloud VM deployment", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.5 Design and Implementation Constraints", h1))
    story.append(Paragraph("• Frontend is built with <b>React 19</b> and <b>Tailwind CSS 3.4</b>", bullet))
    story.append(Paragraph("• Backend uses Python 3.12 with FastAPI asynchronous REST framework", bullet))
    story.append(Paragraph("• JWT tokens expire in <b>24 hours</b> for session security", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 6: Constraints continued, 2.6 Assumptions, 3. User Roles (Reference Page 6)
    # =========================================================================
    story.append(Paragraph("• File uploads for voter CSV import are limited to <b>10 MB</b> per file", bullet))
    story.append(Paragraph("• Allowed file type for bulk voter import: CSV", bullet))
    story.append(Paragraph("• Rate limiting is applied to authentication and vote submission routes", bullet))
    story.append(Paragraph("• CORS is strictly configured to allow only registered frontend domains", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.6 Assumptions and Dependencies", h1))
    story.append(Paragraph("• Users have stable internet connectivity.", bullet))
    story.append(Paragraph("• Every voter possesses a valid unique email and account credentials.", bullet))
    story.append(Paragraph("• Database and custom blockchain ledger services remain active during polling.", bullet))
    story.append(Paragraph("• Cryptographic secret keys for vote encryption and JWT signing are properly secured in environment variables.", bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("3. User Roles & Characteristics", h1))
    story.append(Paragraph("3.1 Admin", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Moderate; expected to use a web-based admin dashboard", bullet))
    story.append(Paragraph("• <b>Access level:</b> Full system access", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> Create elections, add candidates, bulk-enroll voters, monitor metrics, view audit logs", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'admin')", bullet))

    story.append(Paragraph("3.2 Voter", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Basic to moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Scoped to assigned active elections and personal ballot casting", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> View candidates, cast encrypted vote, download QR receipt, verify receipt hash", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'voter')", bullet))

    story.append(Paragraph("3.3 Observer / Election Auditor", h2))
    story.append(Paragraph("• <b>Technical proficiency:</b> Basic to moderate", bullet))
    story.append(Paragraph("• <b>Access level:</b> Read-only access to public transparency metrics", bullet))
    story.append(Paragraph("• <b>Typical tasks:</b> View live results, inspect block ledger, audit cryptographic integrity, view AI fraud alerts", bullet))
    story.append(Paragraph("• <b>Authentication:</b> Stored in User table (role = 'observer')", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 7: Actor Use Cases Table & 4. Functional Requirements - Auth (Reference Page 7)
    # =========================================================================
    actor_uc_data = [
        [Paragraph("Actor", th), Paragraph("Use Cases", th)],
        [Paragraph("Admin", td), Paragraph("Manage Users, Elections, Candidates, Bulk CSV Import, Audit Logs, System Health", td)],
        [Paragraph("Voter", td), Paragraph("View Active Elections, Cast Encrypted Vote, Download QR Receipt, Verify Receipt Hash", td)],
        [Paragraph("Observer / Auditor", td), Paragraph("Live Standings, Audit Blockchain Ledger, Chain Verification, AI Fraud Alerts", td)],
    ]
    t_auc = Table(actor_uc_data, colWidths=[130, 370])
    t_auc.setStyle(ref_table_style)
    story.append(t_auc)
    story.append(Spacer(1, 15))

    story.append(Paragraph("4. Functional Requirements", h1))
    story.append(Paragraph("4.1 Authentication & Authorization Module", h2))

    story.append(Paragraph("<b>FR-AUTH-01: User Login</b>", h2))
    story.append(Paragraph("• <b>Description:</b> The system shall allow admin, voters, and observers to log in using email/username and password.", bullet))
    story.append(Paragraph("• <b>Input:</b> Email/Username, Password", bullet))
    story.append(Paragraph("• <b>Process:</b> System searches user record and verifies password using bcrypt. Returns a JWT access token.", bullet))
    story.append(Paragraph("• <b>Output:</b> JWT access token + user profile data", bullet))
    story.append(Paragraph("• <b>Token Expiry:</b> 24 hours", bullet))
    story.append(Paragraph("• <b>Error Cases:</b> Invalid credentials -> HTTP 400", bullet))

    story.append(Paragraph("<b>FR-AUTH-02: Admin User Creation</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Only authenticated admins can create new user accounts.", bullet))
    story.append(Paragraph("• <b>Input:</b> Username, email, password, role (voter/observer)", bullet))
    story.append(Paragraph("• <b>Process:</b> Admin-authenticated endpoint creates record in User table", bullet))
    story.append(Paragraph("• <b>Validation:</b> Unique email and username required", bullet))

    story.append(Paragraph("<b>FR-AUTH-03: Logout</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Users can log out, clearing local storage JWT token.", bullet))
    story.append(Paragraph("• <b>Process:</b> Token removed from client storage; subsequent requests require re-authentication.", bullet))

    story.append(Paragraph("<b>FR-AUTH-04: Token Verification</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Protected routes verify the Bearer token before proceeding.", bullet))
    story.append(Paragraph("• <b>Process:</b> JWT decoded -> user looked up by ID -> user role validated", bullet))

    story.append(Paragraph("<b>FR-AUTH-05: Password Change</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Users can change their own passwords securely.", bullet))
    story.append(Paragraph("• <b>Input:</b> Current password, new password (min 6 characters)", bullet))
    story.append(Paragraph("• <b>Process:</b> Verify current password -> bcrypt hash new password -> save to database", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 8: 4.2 Admin Dashboard Module (Reference Page 8)
    # =========================================================================
    story.append(Paragraph("4.2 Admin Dashboard Module", h1))
    story.append(Paragraph("<b>FR-ADMIN-01: Dashboard Overview</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin home page displays aggregated metrics:", bullet))
    story.append(Paragraph("  - Total Elections", bullet))
    story.append(Paragraph("  - Active Elections", bullet))
    story.append(Paragraph("  - Total Registered Voters", bullet))
    story.append(Paragraph("  - Total Blockchain Votes Mined", bullet))
    story.append(Paragraph("  - Blockchain Health & Mining Status", bullet))
    story.append(Paragraph("• <b>Data Source:</b> <font name='Courier'>GET /api/v1/admin/metrics</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-02: Election Management</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can create, edit, activate, schedule, and close elections.", bullet))
    story.append(Paragraph("• <b>Operations:</b> List all elections; create new election; update status (draft, active, closed)", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/elections, PUT /api/v1/elections/:id/status</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-03: Candidate Nomination Studio</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can register candidates for an election with full metadata.", bullet))
    story.append(Paragraph("• <b>Fields:</b> Candidate Name, Party / Affiliation, Manifesto Description, Avatar URL", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/elections/:id/candidates</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-04: Bulk Voter Enrollment</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can upload a CSV file to bulk-create voter accounts.", bullet))
    story.append(Paragraph("• <b>CSV Fields:</b> Email, Username, Password", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/admin/import-voters-csv</font>", bullet))

    story.append(Paragraph("<b>FR-ADMIN-05: Immutable Audit Logs</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Admin can view and download immutable audit logs of all user actions.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/admin/audit-logs</font>", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 9: 4.3 Voter Dashboard Module (Reference Page 9)
    # =========================================================================
    story.append(Paragraph("4.3 Voter Dashboard Module", h1))
    story.append(Paragraph("<b>FR-VOTER-01: Active Elections List</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Voter home page displays all active elections and candidate profiles.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/elections</font>", bullet))

    story.append(Paragraph("<b>FR-VOTER-02: 1-Click Encrypted Voting</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Voter selects candidate and casts vote encrypted with AES-256 GCM and signed with single-use ECDSA key pair.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>POST /api/v1/votes/cast</font>", bullet))

    story.append(Paragraph("<b>FR-VOTER-03: Anti-Double Voting Enforcement</b>", h2))
    story.append(Paragraph("• <b>Description:</b> System blocks duplicate vote attempts for the same election and logs violation to security audit trail.", bullet))

    story.append(Paragraph("<b>FR-VOTER-04: Downloadable QR Receipt</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Generates printable QR receipt containing receipt hash, block index, and transaction hash.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/votes/my-receipts</font>", bullet))

    story.append(Paragraph("<b>FR-VOTER-05: Receipt Verification Desk</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Voters can verify any receipt hash against the public blockchain ledger.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/votes/verify-receipt/:hash</font>", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 10: 4.4 Custom Blockchain & 4.5 AI Module (Reference Page 10)
    # =========================================================================
    story.append(Paragraph("4.4 Custom Blockchain Module", h1))
    story.append(Paragraph("<b>FR-CHAIN-01: Proof-of-Work Block Mining</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Automatically packages queued transactions into blocks meeting SHA-256 Proof-of-Work difficulty target (leading zero prefix).", bullet))

    story.append(Paragraph("<b>FR-CHAIN-02: Merkle Tree Generation</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Computes cryptographic binary Merkle Root hash from all transaction hashes in a block.", bullet))

    story.append(Paragraph("<b>FR-CHAIN-03: Ledger Explorer & Tamper Audit</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Public explorer endpoint allowing block browsing, transaction lookup, and 1-click full chain validation.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/blockchain/blocks, GET /api/v1/blockchain/verify-chain</font>", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("4.5 AI Fraud Radar & Anomaly Detection Module", h1))
    story.append(Paragraph("<b>FR-AI-01: Fraud Risk Index & Velocity Analysis</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Analyzes vote velocity bursts (<2s), duplicate IP clusters, and double-voting attempts to output a unified threat score (0-100%).", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/ai/fraud-analysis/:election_id</font>", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 11: 4.6 Observer Dashboard Module (Reference Page 11)
    # =========================================================================
    story.append(Paragraph("4.6 Observer Transparency & Analytics Module", h1))
    story.append(Paragraph("<b>FR-OBSERVER-01: Live Standings & Vote Tallies</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Real-time display of current vote counts, percentages, and leading candidates per election.", bullet))
    story.append(Paragraph("• <b>Route:</b> <font name='Courier'>GET /api/v1/observer/live-results/:election_id</font>", bullet))

    story.append(Paragraph("<b>FR-OBSERVER-02: Recharts Vote Distribution Visualizer</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Interactive bar and pie charts rendering vote distribution and voter turnout percentages.", bullet))

    story.append(Paragraph("<b>FR-OBSERVER-03: Audit Report PDF Export</b>", h2))
    story.append(Paragraph("• <b>Description:</b> Allows election observers to export official election tally and audit certificates.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 12: 5. Non-Functional Requirements - Performance (Reference Page 12)
    # =========================================================================
    story.append(Paragraph("5. Non-Functional Requirements", h1))
    story.append(Paragraph("5.1 Performance", h2))
    nfr_perf_data = [
        [Paragraph("Metric", th), Paragraph("Requirement", th)],
        [Paragraph("API Response Time", td), Paragraph("< 500 milliseconds for standard data endpoints under normal load", td)],
        [Paragraph("File Upload", td), Paragraph("Handles CSV files up to 10 MB; uploads complete within 10 seconds", td)],
        [Paragraph("Block Mining", td), Paragraph("PoW block mined and synced to database within 2 seconds", td)],
        [Paragraph("Real-Time Broadcast", td), Paragraph("WebSocket vote updates pushed to observers within 1 second", td)],
        [Paragraph("Concurrent Users", td), Paragraph("Supports at least 500 concurrent voters in production configuration", td)],
    ]
    t_nfr_p = Table(nfr_perf_data, colWidths=[150, 350])
    t_nfr_p.setStyle(ref_table_style)
    story.append(t_nfr_p)
    story.append(PageBreak())

    # =========================================================================
    # Page 13: 5.2 Security & 5.3 Reliability (Reference Page 13)
    # =========================================================================
    story.append(Paragraph("5.2 Security", h1))
    sec_data = [
        [Paragraph("Requirement", th), Paragraph("Detail", th)],
        [Paragraph("Authentication", td), Paragraph("JWT Bearer tokens, 24-hour expiry", td)],
        [Paragraph("Password Storage", td), Paragraph("bcrypt with salt rounds = 10", td)],
        [Paragraph("Vote Encryption", td), Paragraph("AES-256 GCM symmetric vote payload encryption", td)],
        [Paragraph("Digital Signatures", td), Paragraph("ECDSA SECP256R1 asymmetric key pair signatures", td)],
        [Paragraph("Rate Limiting", td), Paragraph("Auth routes: strict limiter; Vote routes: velocity limiter", td)],
        [Paragraph("CORS", td), Paragraph("Whitelist-only: localhost:3000 and production domain URL", td)],
        [Paragraph("Input Validation", td), Paragraph("Pydantic schemas for all incoming request payloads", td)],
        [Paragraph("SQL Injection Defense", td), Paragraph("SQLAlchemy ORM parameterized queries", td)],
    ]
    t_sec = Table(sec_data, colWidths=[150, 350])
    t_sec.setStyle(ref_table_style)
    story.append(t_sec)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.3 Reliability", h2))
    story.append(Paragraph("• System maintains <b>99.9% uptime</b> during voting windows. Immutable blockchain ledger guarantees zero vote loss or record modification.", bullet))

    story.append(Paragraph("5.4 Usability", h2))
    story.append(Paragraph("• Responsive layout built with Tailwind CSS — supports desktop, tablet, and mobile browsers with dark/light mode toggle.", bullet))

    story.append(Paragraph("5.5 Scalability", h2))
    story.append(Paragraph("• Stateless JWT authentication and relational database indexing support horizontal backend scaling.", bullet))

    story.append(Paragraph("5.6 Maintainability", h2))
    story.append(Paragraph("• Clear architectural separation of concerns: API Routes -> Services -> Blockchain Core -> Database Models.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Page 14: 6. System Constraints & 7. External Interfaces (Reference Page 14)
    # =========================================================================
    story.append(Paragraph("6. System Constraints", h1))
    story.append(Paragraph("22. Blockchain Proof-of-Work difficulty target is set to 2 leading zeros for lightweight execution.", bullet))
    story.append(Paragraph("23. File uploads for voter CSV enrollment are restricted to CSV format under 10 MB.", bullet))
    story.append(Paragraph("24. Single vote policy strictly enforced per voter per election via compound database uniqueness.", bullet))
    story.append(Paragraph("25. Vote payloads are encrypted at rest using server-side AES-256 GCM secret key.", bullet))
    story.append(Paragraph("26. Token Blacklist operates in-memory with client-side localStorage cleanup.", bullet))
    story.append(Paragraph("27. Real-time push updates require WebSocket client compatibility.", bullet))

    story.append(Spacer(1, 15))
    story.append(Paragraph("7. External Interface Requirements", h1))
    story.append(Paragraph("7.1 User Interfaces", h2))
    ui_data = [
        [Paragraph("Page", th), Paragraph("Role", th), Paragraph("Description", th)],
        [Paragraph("Login / Register", td), Paragraph("Public", td), Paragraph("Authentication portal with role selector (Admin, Voter, Observer)", td)],
        [Paragraph("Admin Dashboard", td), Paragraph("Admin", td), Paragraph("Sidebar with Overview, Elections CRUD, Candidates, CSV Import, Audit", td)],
        [Paragraph("Voter Dashboard", td), Paragraph("Voter", td), Paragraph("Active Ballots, 1-Click Encrypted Voting, QR Receipts, Verification", td)],
        [Paragraph("Observer Dashboard", td), Paragraph("Observer", td), Paragraph("Live Recharts standings, Vote Distribution, Turnout Percentages", td)],
        [Paragraph("Blockchain Explorer", td), Paragraph("Public", td), Paragraph("Mined Blocks, Transaction Lookup, 1-Click Tamper Auditor", td)],
        [Paragraph("AI Fraud Radar", td), Paragraph("Admin/Observer", td), Paragraph("Real-time velocity spikes, duplicate IP clusters, Threat Index", td)],
    ]
    t_ui = Table(ui_data, colWidths=[120, 90, 290])
    t_ui.setStyle(ref_table_style)
    story.append(t_ui)
    story.append(PageBreak())

    # =========================================================================
    # Page 15: 7.2 - 8.1 Data Entities (Reference Page 15)
    # =========================================================================
    story.append(Paragraph("7.2 Hardware Interfaces", h2))
    story.append(Paragraph("• Standard web-enabled client hardware (PC, Laptop, Tablet, Smartphone)", bullet))

    story.append(Paragraph("7.3 Software Interfaces", h2))
    sw_data = [
        [Paragraph("System", th), Paragraph("Interface", th)],
        [Paragraph("SQLite / PostgreSQL", td), Paragraph("SQLAlchemy ORM connection protocol", td)],
        [Paragraph("FastAPI WebSockets", td), Paragraph("Real-time bidirectional event manager", td)],
        [Paragraph("Vercel / Docker", td), Paragraph("Static CDN hosting and containerized ASGI backend", td)],
    ]
    t_sw = Table(sw_data, colWidths=[150, 350])
    t_sw.setStyle(ref_table_style)
    story.append(t_sw)

    story.append(Spacer(1, 10))
    story.append(Paragraph("7.4 Communication Interfaces", h2))
    story.append(Paragraph("• <b>Protocol:</b> HTTPS (production), HTTP (local development)", bullet))
    story.append(Paragraph("• <b>Data Format:</b> JSON (REST API & WebSockets)", bullet))
    story.append(Paragraph("• <b>Auth Header:</b> Authorization: Bearer &lt;JWT_TOKEN&gt;", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Data Requirements", h1))
    story.append(Paragraph("8.1 Data Entities", h2))
    de_data = [
        [Paragraph("Entity", th), Paragraph("Collection / Table", th), Paragraph("Key Fields", th)],
        [Paragraph("User", td), Paragraph("users", td), Paragraph("id, email, username, hashed_password, role, is_active, created_at", td)],
        [Paragraph("Election", td), Paragraph("elections", td), Paragraph("id, title, description, status, start_time, end_time, created_by", td)],
        [Paragraph("Candidate", td), Paragraph("candidates", td), Paragraph("id, election_id, name, party, manifesto, avatar_url, vote_count", td)],
        [Paragraph("Vote", td), Paragraph("votes", td), Paragraph("id, user_id, election_id, candidate_id, voter_hash, tx_hash, block_index, receipt_hash", td)],
        [Paragraph("Block", td), Paragraph("blocks", td), Paragraph("id, index, timestamp, previous_hash, hash, nonce, merkle_root, signature", td)],
        [Paragraph("Transaction", td), Paragraph("transactions", td), Paragraph("id, tx_hash, block_index, election_id, voter_hash, encrypted_vote, signature", td)],
        [Paragraph("Audit Log", td), Paragraph("audit_logs", td), Paragraph("id, user_id, user_email, action, details, ip_address, timestamp", td)],
    ]
    t_de = Table(de_data, colWidths=[85, 95, 320])
    t_de.setStyle(ref_table_style)
    story.append(t_de)
    story.append(PageBreak())

    # =========================================================================
    # Page 16: 8.2 Data Retention & 8.3 Data Integrity (Reference Page 16)
    # =========================================================================
    story.append(Paragraph("8.2 Data Retention", h1))
    story.append(Paragraph("• Security audit logs and voter activity logs are timestamped and preserved for election verification.", bullet))
    story.append(Paragraph("• Blockchain blocks and vote transactions are immutable — once mined into the ledger, records persist permanently.", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8.3 Data Integrity", h1))
    story.append(Paragraph("• Unique email and username constraints on User collection prevent duplicate accounts.", bullet))
    story.append(Paragraph("• Unique compound constraint on Vote (user_id, election_id) guarantees single vote enforcement.", bullet))
    story.append(Paragraph("• Unique cryptographic hashes on Block (index, hash) and Transaction (tx_hash) guarantee tamper-evident ledger integrity.", bullet))

    # Build PDF Document
    doc.build(story)
    print(f"Successfully generated standalone SRS PDF at: {filename}")

if __name__ == "__main__":
    generate_srs_pdf()
