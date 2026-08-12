import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def generate_exact_16page_srs(filename="docs/Blockchain_Voting_System_SRS.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 45pt margins (~0.625 in) giving crisp layout on Letter / A4
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Exact Colors from the Reference PDF
    COLOR_TEAL = colors.HexColor("#008080")       # Teal for Subtitles & Accents
    COLOR_NAVY = colors.HexColor("#1B365D")       # Navy for Main Headings & Table Headers
    COLOR_DARK = colors.HexColor("#222222")       # Dark Charcoal for Body text
    COLOR_BORDER = colors.HexColor("#000000")     # Black/Dark Grey borders

    # Typography Matching the Reference PDF
    title_teal = ParagraphStyle(
        'TitleTeal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=COLOR_TEAL
    )

    main_title_navy = ParagraphStyle(
        'MainTitleNavy',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=TA_CENTER,
        textColor=COLOR_NAVY
    )

    sub_title_navy = ParagraphStyle(
        'SubTitleNavy',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=TA_CENTER,
        textColor=COLOR_NAVY
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=17,
        alignment=TA_CENTER,
        textColor=COLOR_DARK
    )

    h1 = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=18,
        spaceBefore=10,
        spaceAfter=3,
        textColor=COLOR_NAVY
    )

    h2 = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        spaceBefore=7,
        spaceAfter=3,
        textColor=COLOR_TEAL
    )

    h2_navy = ParagraphStyle(
        'Heading2Navy',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        spaceBefore=7,
        spaceAfter=3,
        textColor=COLOR_NAVY
    )

    body = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        spaceAfter=3,
        alignment=TA_LEFT,
        textColor=COLOR_DARK
    )

    bullet = ParagraphStyle(
        'BulletText',
        parent=body,
        leftIndent=12,
        spaceAfter=2.5
    )

    num_bullet = ParagraphStyle(
        'NumBulletText',
        parent=body,
        leftIndent=12,
        spaceAfter=3
    )

    th = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    td = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=COLOR_DARK
    )

    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=COLOR_DARK
    )

    # Reference Navy-Header Table Style
    navy_table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    # Plain Border Table Style for TOC
    toc_table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE (Exact match to Reference Screenshot Page 1)
    # =========================================================================
    story.append(Spacer(1, 120))
    story.append(Paragraph("Software Requirements Specification (SRS)", title_teal))
    story.append(Spacer(1, 28))
    story.append(Paragraph("BLOCKCHAIN VOTING SYSTEM", main_title_navy))
    story.append(Spacer(1, 6))
    story.append(Paragraph("CRYPTOGRAPHIC E-VOTING & DECENTRALIZED LEDGER", sub_title_navy))
    story.append(Spacer(1, 35))

    meta_content = """
    <b>Document Version:</b> 1.0<br/><br/>
    <b>Prepared By:</b> Aditya Yadav<br/><br/>
    <b>Institution:</b> TRCAC (Thakur Ramnarayan College of Arts & Commerce)<br/><br/>
    <b>Department:</b> B.Sc. Computer Science<br/><br/>
    <b>Academic Year:</b> 2026–2027<br/><br/>
    <b>Date:</b> August 2026<br/><br/>
    <b>Status:</b> Final Draft
    """
    story.append(Paragraph(meta_content, meta_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS (Exact match to Reference Screenshot Page 2)
    # =========================================================================
    story.append(Paragraph("Table of Contents", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=15))

    toc_data = [
        [Paragraph("<b>Sr.<br/>No.</b>", td_bold), Paragraph("<b>Main Section</b>", td_bold), Paragraph("<b>Description</b>", td_bold)],
        [Paragraph("1", td), Paragraph("<b>Introduction</b>", td_bold), Paragraph("Introduces the project, its purpose, scope, audience, and references.", td)],
        [Paragraph("2", td), Paragraph("<b>Overall Description</b>", td_bold), Paragraph("Provides an overview of the system, modules, workflow, and operating environment.", td)],
        [Paragraph("3", td), Paragraph("<b>User Roles &<br/>Characteristics</b>", td_bold), Paragraph("Describes different user roles and their responsibilities within the system.", td)],
        [Paragraph("4", td), Paragraph("<b>Functional<br/>Requirements</b>", td_bold), Paragraph("Defines all core features and functions that the system must perform.", td)],
        [Paragraph("5", td), Paragraph("<b>Non-Functional<br/>Requirements</b>", td_bold), Paragraph("Specifies performance, security, reliability, usability, scalability, and maintainability requirements.", td)],
        [Paragraph("6", td), Paragraph("<b>System Constraints</b>", td_bold), Paragraph("Lists technical limitations, assumptions, and development constraints.", td)],
        [Paragraph("7", td), Paragraph("<b>External Interface<br/>Requirements</b>", td_bold), Paragraph("Describes the user interface, page structure, and interactions with external components.", td)],
        [Paragraph("8", td), Paragraph("<b>Data Requirements</b>", td_bold), Paragraph("Defines database entities, data structures, relationships, and storage requirements.", td)],
    ]
    t_toc = Table(toc_data, colWidths=[35, 140, 325])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: 1. INTRODUCTION, 1.1 PURPOSE, 1.2 SCOPE, 1.3 AUDIENCE (Page 3)
    # =========================================================================
    story.append(Paragraph("1. Introduction", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("1.1 Purpose", h2))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) document defines the functional and non-functional "
        "requirements for the Blockchain Voting System (BVS). The system is designed to digitise, secure, and streamline "
        "the complete election cycle — encompassing voter registration, candidate nomination, 1-click encrypted voting, "
        "Proof-of-Work block mining, and verifiable cryptographic receipts.",
        body
    ))
    story.append(Paragraph(
        "This document serves as the primary reference for developers, project managers, QA engineers, and institutional "
        "administration throughout the system development lifecycle.",
        body
    ))

    story.append(Paragraph("1.2 Project Scope", h2))
    story.append(Paragraph(
        "The Blockchain Voting System is a web-based multi-role application that centralises the end-to-end election "
        "operations. The system replaces manual, paper-based, and centralized database processes with a unified, "
        "role-driven platform that ensures data integrity, operational visibility, and tamper-evident vote recording.",
        body
    ))
    story.append(Paragraph("The system covers the following operational domains:", body))
    story.append(Paragraph("● User profile and voter eligibility management", bullet))
    story.append(Paragraph("● Election scheduling and lifecycle state management", bullet))
    story.append(Paragraph("● Candidate registration and manifesto management", bullet))
    story.append(Paragraph("● 1-Click encrypted ballot casting with AES-256 GCM encryption", bullet))
    story.append(Paragraph("● Asymmetric digital signature signing via ECDSA SECP256R1", bullet))
    story.append(Paragraph("● Proof-of-Work block mining and binary Merkle Tree computation", bullet))
    story.append(Paragraph("● Downloadable QR code receipts and hash verification desk", bullet))
    story.append(Paragraph("● AI Fraud Radar tracking vote velocity bursts and duplicate IP clusters", bullet))
    story.append(Paragraph("● Real-time election standings and audit trail logging", bullet))

    story.append(Paragraph("1.3 Intended Audience", h2))
    aud_data = [
        [Paragraph("Audience", th), Paragraph("Usage", th)],
        [Paragraph("Software Development Team", td), Paragraph("Design, develop, and integrate system modules per specifications", td)],
        [Paragraph("Project Manager", td), Paragraph("Track deliverables, milestones, and scope boundaries", td)],
        [Paragraph("QA / Testing Team", td), Paragraph("Derive test cases and acceptance criteria", td)],
        [Paragraph("Institutional Administration", td), Paragraph("Validate that requirements reflect institutional election needs", td)],
        [Paragraph("Election Officer / Auditor", td), Paragraph("Primary end-user; manages day-to-day elections and reviews audit logs", td)],
        [Paragraph("System Administrator", td), Paragraph("Understand roles, access levels, and security policies", td)],
    ]
    t_aud = Table(aud_data, colWidths=[160, 340])
    t_aud.setStyle(navy_table_style)
    story.append(t_aud)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: 1.4 DEFINITIONS & ABBREVIATIONS, 1.5 REFERENCES (Page 4)
    # =========================================================================
    story.append(Paragraph("1.4 Definitions and Abbreviations", h2))
    def_data = [
        [Paragraph("Term / Acronym", th), Paragraph("Definition", th)],
        [Paragraph("BVS", td), Paragraph("Blockchain Voting System", td)],
        [Paragraph("PoW", td), Paragraph("Proof-of-Work — consensus algorithm for computational block mining", td)],
        [Paragraph("ECDSA", td), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1 curve)", td)],
        [Paragraph("AES-256 GCM", td), Paragraph("Advanced Encryption Standard with Galois/Counter Mode authenticated encryption", td)],
        [Paragraph("SHA-256", td), Paragraph("Secure Hash Algorithm 256-bit cryptographic digest function", td)],
        [Paragraph("Merkle Tree", td), Paragraph("Cryptographic binary hash tree aggregating all transactions within a block", td)],
        [Paragraph("SRS", td), Paragraph("Software Requirements Specification", td)],
        [Paragraph("RBAC", td), Paragraph("Role-Based Access Control", td)],
        [Paragraph("JWT", td), Paragraph("JSON Web Token — stateless cryptographic bearer token for authentication", td)],
        [Paragraph("FK / PK", td), Paragraph("Foreign Key / Primary Key — database relational identifiers", td)],
        [Paragraph("TRCAC", td), Paragraph("Thakur Ramnarayan College of Arts & Commerce", td)],
    ]
    t_def = Table(def_data, colWidths=[130, 370])
    t_def.setStyle(navy_table_style)
    story.append(t_def)
    story.append(Spacer(1, 14))

    story.append(Paragraph("1.5 References", h2))
    story.append(Paragraph("● IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications", bullet))
    story.append(Paragraph("● ISO/IEC 25010:2011: Systems and Software Quality Requirements and Evaluation", bullet))
    story.append(Paragraph("● OWASP Security Guidelines for Web Applications", bullet))
    story.append(Paragraph("● NIST Special Publication 800-38D (GCM Block Cipher Mode)", bullet))
    story.append(Paragraph("● SEC 2: Recommended Elliptic Curve Domain Parameters (SECP256R1)", bullet))
    story.append(Paragraph("● Tailwind CSS and React 19 Component Library Documentation", bullet))
    story.append(Paragraph("● FastAPI Asynchronous Web Framework Documentation", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: 2. OVERALL DESCRIPTION, 2.1 CONTEXT, 2.2 MODULES, 2.3 WORKFLOW (Page 5)
    # =========================================================================
    story.append(Paragraph("2. Overall Description", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("2.1 System Context", h2))
    story.append(Paragraph(
        "The BVS is a centralised, browser-based platform accessible via standard browsers on desktop, tablet, "
        "and mobile devices. The system integrates multiple operational modules under a single authentication layer, "
        "with all relational application data persisted in a database and vote transactions secured in an immutable "
        "custom Python Blockchain ledger.",
        body
    ))

    story.append(Paragraph("2.2 System Modules", h2))
    mod_data = [
        [Paragraph("#", th), Paragraph("Module", th), Paragraph("Responsibility", th)],
        [Paragraph("1", td), Paragraph("User Management", td), Paragraph("Handles user registration, authentication, and role assignment", td)],
        [Paragraph("2", td), Paragraph("Election Management", td), Paragraph("Manages election creation, scheduling, and status lifecycle", td)],
        [Paragraph("3", td), Paragraph("Candidate Management", td), Paragraph("Registers candidates, stores manifestos, party, and avatars", td)],
        [Paragraph("4", td), Paragraph("Voting & Encryption", td), Paragraph("Voter casts AES-256 encrypted ballots with ECDSA signatures", td)],
        [Paragraph("5", td), Paragraph("Blockchain Engine", td), Paragraph("Packages transactions, mines PoW blocks, and generates Merkle roots", td)],
        [Paragraph("6", td), Paragraph("Receipt & Verification", td), Paragraph("Generates QR receipts and verifies receipt hashes on the ledger", td)],
        [Paragraph("7", td), Paragraph("AI Fraud Radar", td), Paragraph("Detects vote velocity bursts (<2s), IP clusters, and risk score", td)],
        [Paragraph("8", td), Paragraph("Observer & Analytics", td), Paragraph("Real-time vote counts, turnout percentages, and Recharts charts", td)],
        [Paragraph("9", td), Paragraph("Reports & Audit", td), Paragraph("Immutable audit logs, system metrics, and export to CSV", td)],
    ]
    t_mod = Table(mod_data, colWidths=[25, 145, 330])
    t_mod.setStyle(navy_table_style)
    story.append(t_mod)

    story.append(Paragraph("2.3 System Workflow", h2))
    story.append(Paragraph("The following sequence describes the standard end-to-end operational flow within the Blockchain Voting System:", body))
    workflows = [
        "1. Administrator logs in and creates user accounts, assigning appropriate roles (Admin, Voter, Observer).",
        "2. Voters and Observers log in using their credentials and receive a stateless 24-hour JWT token.",
        "3. Administrator creates new elections, sets start/end dates, and adds candidate profiles with manifestos.",
        "4. Administrator uploads voter CSV files to bulk-enroll eligible voters.",
        "5. Voters browse active elections, review candidate manifestos, and select their preferred candidate.",
        "6. The system encrypts the vote payload using AES-256 GCM and signs the transaction with single-use ECDSA keypair.",
        "7. Blockchain Engine validates single-vote rule, queues transaction, and triggers Proof-of-Work block mining.",
        "8. Block is mined with SHA-256 difficulty target, computes binary Merkle root, and persists to ledger.",
        "9. Voter receives a downloadable QR receipt containing receipt hash, block index, and transaction hash.",
        "10. AI Fraud Radar continuously analyzes submission timestamps and flags anomaly risk scores (0-100%).",
        "11. Observers and Administrator review live Recharts standings and export official audit reports.",
    ]
    for wf in workflows:
        story.append(Paragraph(wf, num_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 3. USER ROLES & 4. FUNCTIONAL REQUIREMENTS (4.1 to 4.3) (Page 6)
    # =========================================================================
    story.append(Paragraph("3. User Roles & Characteristics", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("3.1 User Roles Summary", h2))
    role_summary_data = [
        [Paragraph("Role", th), Paragraph("System Responsibilities", th)],
        [Paragraph("Administrator", td), Paragraph("Full system access; manages users, roles, elections, candidates, bulk CSV voter enrollment, and platform configuration", td)],
        [Paragraph("Voter", td), Paragraph("Views active elections, reviews candidates, casts encrypted votes, downloads QR receipts, and verifies hashes", td)],
        [Paragraph("Observer / Auditor", td), Paragraph("Monitors live standings, inspects block explorer, audits blockchain integrity, and views AI fraud alerts", td)],
    ]
    t_rs = Table(role_summary_data, colWidths=[130, 370])
    t_rs.setStyle(navy_table_style)
    story.append(t_rs)

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. Functional Requirements", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.1 User Management", h2))
    u_funcs = [
        "1. The system shall provide a secure login mechanism using email/username and password credentials with encrypted password storage (bcrypt).",
        "2. The system shall allow the Administrator to create, view, update, and deactivate user accounts.",
        "3. Each user shall be assigned exactly one role from the predefined role set (Admin, Voter, Observer).",
        "4. The system shall restrict access to modules and pages based on the authenticated user's assigned role.",
        "5. The system shall maintain a security log recording every user login and logout event with timestamp and IP address.",
    ]
    for uf in u_funcs:
        story.append(Paragraph(uf, num_bullet))

    story.append(Paragraph("4.2 Election Management", h2))
    e_funcs = [
        "1. The system shall allow Administrator to create elections with title, description, start time, and end time.",
        "2. The system shall allow Administrator to transition election status between Draft, Active, and Closed.",
        "3. The system shall automatically filter and display active elections to registered voters.",
        "4. The system shall prevent voting on elections that are in Draft or Closed status.",
    ]
    for ef in e_funcs:
        story.append(Paragraph(ef, num_bullet))

    story.append(Paragraph("4.3 Candidate Management", h2))
    c_funcs = [
        "1. The system shall allow Administrator to register candidates with name, party/affiliation, manifesto, and avatar URL.",
    ]
    for cf in c_funcs:
        story.append(Paragraph(cf, num_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: 4. FUNCTIONAL REQUIREMENTS (4.4 to 4.8) (Page 7)
    # =========================================================================
    c_funcs_cont = [
        "2. The system shall store candidate-wise profile details and manifestos.",
        "3. The system shall display candidate profiles on the voter ballot with manifesto preview popups.",
    ]
    for cf in c_funcs_cont:
        story.append(Paragraph(cf, num_bullet))

    story.append(Paragraph("4.4 Job Posting & Voting Application (Voting Module)", h2))
    v_funcs = [
        "1. The system shall allow eligible voters to select a candidate and cast an encrypted vote.",
        "2. The system shall encrypt the vote payload using AES-256 GCM authenticated symmetric encryption before storage.",
        "3. The system shall digitally sign each vote transaction using a single-use ECDSA SECP256R1 keypair.",
        "4. The system shall strictly enforce a single vote per registered voter per election, blocking duplicate attempts.",
    ]
    for vf in v_funcs:
        story.append(Paragraph(vf, num_bullet))

    story.append(Paragraph("4.5 Blockchain Engine & Block Mining", h2))
    b_funcs = [
        "1. The system shall package queued vote transactions into blocks meeting SHA-256 Proof-of-Work difficulty targets.",
        "2. The system shall compute a cryptographic binary Merkle Root from all transaction hashes in each block.",
        "3. The system shall maintain an immutable block chain linked by cryptographic SHA-256 previous block hashes.",
        "4. The system shall provide a 1-click ledger audit function that verifies chain integrity and detects tampering.",
    ]
    for bf in b_funcs:
        story.append(Paragraph(bf, num_bullet))

    story.append(Paragraph("4.6 Receipt Generation & Verification", h2))
    r_funcs = [
        "1. The system shall generate a downloadable QR code receipt containing receipt hash, block index, and transaction hash.",
        "2. The system shall allow voters and auditors to verify any receipt hash against the public blockchain ledger.",
        "3. The system shall confirm whether a verified receipt hash is recorded in a valid mined block.",
    ]
    for rf in r_funcs:
        story.append(Paragraph(rf, num_bullet))

    story.append(Paragraph("4.7 AI Fraud Radar & Anomaly Detection", h2))
    ai_funcs = [
        "1. The system shall track vote submission timestamps and client IP addresses in real time.",
        "2. The system shall detect velocity bursts (<2 seconds between votes) and flag automated bot submissions.",
        "3. The system shall detect duplicate IP clusters exceeding configurable threshold limits.",
        "4. The system shall calculate a composite Fraud Risk Index (0-100%) and assign a threat level (Low, Medium, High, Critical).",
    ]
    for af in ai_funcs:
        story.append(Paragraph(af, num_bullet))

    story.append(Paragraph("4.8 Reports & Analytics", h2))
    rep_funcs = [
        "1. The system shall display real-time live standings, vote counts, leading candidates, and turnout percentages.",
        "2. The system shall render interactive bar and pie charts using Recharts for visual analytics.",
        "3. The system shall allow export of election results and audit logs to CSV format.",
    ]
    for rf in rep_funcs:
        story.append(Paragraph(rf, num_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: 5. NON-FUNCTIONAL REQUIREMENTS (Page 8)
    # =========================================================================
    story.append(Paragraph("5. Non-Functional Requirements", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("5.1 Security", h2))
    story.append(Paragraph("● All user passwords shall be stored using a strong cryptographic hashing algorithm (bcrypt with salt rounds = 10). Plain-text storage is strictly prohibited.", bullet))
    story.append(Paragraph("● All HTTP communications shall be enforced over HTTPS (TLS 1.2 or higher).", bullet))
    story.append(Paragraph("● Vote payloads shall be encrypted with AES-256 GCM authenticated encryption.", bullet))
    story.append(Paragraph("● Transaction authenticity shall be enforced via ECDSA SECP256R1 asymmetric key pair signatures.", bullet))
    story.append(Paragraph("● Session tokens shall be stateless JWT Bearer tokens expiring after 24 hours.", bullet))
    story.append(Paragraph("● All page endpoints shall enforce server-side role-based access control. Client-side restrictions alone are not sufficient.", bullet))
    story.append(Paragraph("● The system shall log all login attempts (successful and failed) to the Security Log.", bullet))

    story.append(Paragraph("5.2 Performance", h2))
    story.append(Paragraph("● Standard page loads and API responses shall complete within 500 milliseconds under normal network conditions.", bullet))
    story.append(Paragraph("● Proof-of-Work block mining shall complete within 2 seconds under difficulty target = 2.", bullet))
    story.append(Paragraph("● The system shall support at least 500 concurrent active users without performance degradation.", bullet))
    story.append(Paragraph("● Real-time WebSocket vote broadcasts shall be pushed to client dashboards within 1 second.", bullet))

    story.append(Paragraph("5.3 Usability", h2))
    story.append(Paragraph("● The interface shall require no specialist technical training. A new user shall be able to complete core tasks within their role after a 2-minute orientation.", bullet))
    story.append(Paragraph("● All forms shall display inline validation feedback before or immediately upon submission.", bullet))
    story.append(Paragraph("● All data tables shall support sorting, column filtering, and pagination with a configurable page size.", bullet))
    story.append(Paragraph("● The application shall be fully functional on modern browsers — Chrome, Firefox, Edge, Safari.", bullet))

    story.append(Paragraph("5.4 Reliability and Availability", h2))
    story.append(Paragraph("● The system shall target 99.9% uptime during active election windows.", bullet))
    story.append(Paragraph("● Immutable blockchain ledger structure guarantees zero vote record deletion or unauthorized alteration.", bullet))
    story.append(Paragraph("● The system shall implement graceful error handling — unexpected errors shall display a user-friendly message rather than a raw stack trace.", bullet))

    story.append(Paragraph("5.5 Scalability", h2))
    story.append(Paragraph("● The application architecture shall support horizontal scaling to accommodate increased load during peak voting hours.", bullet))
    story.append(Paragraph("● The database schema shall be extensible to support future modules without breaking existing functionality.", bullet))

    story.append(Paragraph("5.6 Maintainability", h2))
    story.append(Paragraph("● All source code shall follow a consistent coding standard and include inline documentation for complex logic.", bullet))
    story.append(Paragraph("● The application shall be structured using a modular MVC architectural pattern to facilitate independent module updates.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: 6. SYSTEM CONSTRAINTS (Page 9)
    # =========================================================================
    story.append(Paragraph("6. System Constraints", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("6.1 Constraints", h2))
    story.append(Paragraph("● The system shall be built using React 19 and Tailwind CSS as the primary frontend UI framework.", bullet))
    story.append(Paragraph("● The system shall use Python 3.12 with FastAPI as the backend REST API framework.", bullet))
    story.append(Paragraph("● The system shall use a relational database management system (SQLite / PostgreSQL or equivalent).", bullet))
    story.append(Paragraph("● The custom blockchain Proof-of-Work difficulty target shall be configured to 2 leading zeros for lightweight execution.", bullet))
    story.append(Paragraph("● Voter CSV enrollment uploads shall be limited to CSV format with a maximum file size of 10 MB.", bullet))
    story.append(Paragraph("● Vote attempts are strictly limited to one vote per registered voter per election, enforced by unique compound database constraints.", bullet))

    story.append(Paragraph("6.2 Assumptions", h2))
    story.append(Paragraph("● Each user is assigned a single role (Admin, Voter, or Observer). Multi-role access per user account is not required in version 1.0.", bullet))
    story.append(Paragraph("● Network connectivity is stable within the operating infrastructure.", bullet))
    story.append(Paragraph("● User devices (computers and tablets) will have modern evergreen browsers installed.", bullet))
    story.append(Paragraph("● The operating environment will provide secure server infrastructure with protected environment variables (SECRET_KEY, VOTE_ENCRYPTION_KEY).", bullet))
    story.append(Paragraph("● Registered voters possess unique email addresses and valid login credentials.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 7. EXTERNAL INTERFACE REQUIREMENTS & 7.2 PAGE INVENTORY (Page 10)
    # =========================================================================
    story.append(Paragraph("7. External Interface Requirements", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("7.1 UI Design Philosophy", h2))
    story.append(Paragraph(
        "The system interface shall be designed to professional enterprise standards, prioritising clarity, "
        "navigational consistency, and operational efficiency.",
        body
    ))
    story.append(Paragraph("● Clean, structured layout with a fixed top navigation bar and a collapsible left sidebar for module navigation.", bullet))
    story.append(Paragraph("● Dashboard-first approach — the default landing view provides an at-a-glance operational summary for the logged-in role.", bullet))
    story.append(Paragraph("● Data-heavy pages shall use well-styled responsive tables with column sorting, pagination, and search/filter capability.", bullet))
    story.append(Paragraph("● All forms shall use inline validation feedback to minimise input errors.", bullet))
    story.append(Paragraph("● Status indicators shall use coloured badge combinations so information is never conveyed by colour alone.", bullet))
    story.append(Paragraph("● The overall aesthetic should be modern and professional — clean whites, dark modes, navy accents, and teal highlights.", bullet))

    story.append(Paragraph("7.2 Page Inventory and Role Mapping", h2))
    page_inv_data = [
        [Paragraph("#", th), Paragraph("Page Name", th), Paragraph("Accessible By", th), Paragraph("Primary Purpose", th)],
        [Paragraph("1", td), Paragraph("Login / Register", td), Paragraph("All (unauthenticated)", td), Paragraph("Authenticate users and route to dashboard", td)],
        [Paragraph("2", td), Paragraph("Dashboard", td), Paragraph("All Roles (post-login)", td), Paragraph("Centralised operational overview tailored per role", td)],
        [Paragraph("3", td), Paragraph("User Management", td), Paragraph("Admin only", td), Paragraph("Full control over user accounts and role assignments", td)],
        [Paragraph("4", td), Paragraph("Election Management", td), Paragraph("Admin only", td), Paragraph("Create, schedule, activate, and close elections", td)],
        [Paragraph("5", td), Paragraph("Candidate Studio", td), Paragraph("Admin only", td), Paragraph("Register and manage candidate profiles and manifestos", td)],
        [Paragraph("6", td), Paragraph("Bulk Voter Import", td), Paragraph("Admin only", td), Paragraph("Upload CSV files to bulk-enroll voters", td)],
        [Paragraph("7", td), Paragraph("Voter Dashboard", td), Paragraph("Voter only", td), Paragraph("Active elections list, ballot casting, and voting history", td)],
        [Paragraph("8", td), Paragraph("QR Vote Receipt", td), Paragraph("Voter only", td), Paragraph("Download and print cryptographic QR vote receipt", td)],
        [Paragraph("9", td), Paragraph("Receipt Verification", td), Paragraph("All Roles", td), Paragraph("Public verification desk to check receipt hash against ledger", td)],
        [Paragraph("10", td), Paragraph("Blockchain Explorer", td), Paragraph("All Roles", td), Paragraph("Inspect mined blocks, transactions, and trigger chain audit", td)],
        [Paragraph("11", td), Paragraph("Observer Dashboard", td), Paragraph("Observer, Admin", td), Paragraph("Live Recharts standings, vote percentages, and turnout", td)],
        [Paragraph("12", td), Paragraph("AI Fraud Radar", td), Paragraph("Admin, Observer", td), Paragraph("Real-time velocity monitoring and anomaly risk score", td)],
    ]
    t_pi = Table(page_inv_data, colWidths=[20, 110, 110, 260])
    t_pi.setStyle(navy_table_style)
    story.append(t_pi)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: 7.3 PAGE-BY-PAGE DESIGN SPECIFICATION (PAGES 1 TO 6) (Page 11)
    # =========================================================================
    story.append(Paragraph("7.3 Page-by-Page Design Specification", h2))

    pages_p1_6 = [
        ("Page 1 — Login / Register",
         "The Login page is the entry point of the application. It shall be a centred, modern card layout. The card shall contain the application logo and name at the top, followed by Email and Password fields, quick demo role login buttons, and a Login button.",
         "All users (unauthenticated)",
         "Form submission, role selection, field validation, redirect on success"),
        ("Page 2 — Dashboard",
         "The Dashboard is the primary landing page for all authenticated roles. The layout consists of a fixed top navbar, a collapsible left sidebar, and a main content area dynamically tailored to the logged-in role. Admin sees summary stat cards, a blockchain mining health widget, and quick-action buttons; Voters see Active Ballots; Observers see live election standings.",
         "All Roles",
         "Navigation, stat card drill-downs, quick actions"),
        ("Page 3 — User Management (Admin Only)",
         "This page is restricted to the Administrator. It presents a full-page data table of all registered users with columns for name, email, role, and account status. A prominent Add User button opens a modal with the new user form (Name, Email, Password, Role selector). Row-level action buttons allow editing user details, reassigning roles, and deactivating accounts.",
         "Admin",
         "Add user modal, edit user, deactivate with confirmation"),
        ("Page 4 — Election Management",
         "A searchable, filterable table of all elections with columns for title, start date, end date, candidate count, and status badges. The Admin can create elections, activate voting, and close elections. Each row provides an Edit and View Candidates option.",
         "Admin",
         "Create election modal, status toggle, filter by status"),
        ("Page 5 — Candidate Studio",
         "A list of all registered candidates with their party affiliation, manifesto, and avatar image. A prominent Add Candidate button opens a form. Individual candidate rows provide an Edit option and ballot preview.",
         "Admin",
         "Add candidate, edit candidate, delete candidate, view ballot preview"),
        ("Page 6 — Bulk Voter Import",
         "The Bulk Voter Import page allows administrators to upload a CSV file containing voter records (email, username, password). The system validates the CSV in real-time, displays a preview, and imports accounts in a single batch with progress tracking.",
         "Admin",
         "Upload CSV file, review preview, confirm batch import"),
    ]

    for p_title, p_desc, p_acc, p_int in pages_p1_6:
        story.append(Paragraph(f"<b>{p_title}</b>", h2_navy))
        story.append(Paragraph(p_desc, body))
        story.append(Paragraph(f"<b>Accessible By:</b> {p_acc}", body))
        story.append(Paragraph(f"<b>Interactions:</b> {p_int}", body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: 7.3 PAGE-BY-PAGE DESIGN SPECIFICATION (PAGES 7 TO 12) (Page 12)
    # =========================================================================
    pages_p7_12 = [
        ("Page 7 — Voter Dashboard",
         "Shows active elections available to the voter. Displays candidate cards with photos, party emblems, and a View Manifesto button. The voter can select a candidate and cast a 1-click encrypted ballot with confirmation dialog.",
         "Voter",
         "View candidates, read manifesto, cast encrypted vote"),
        ("Page 8 — QR Vote Receipt",
         "A cryptographic receipt page rendered immediately after voting. Displays the receipt hash, block index, timestamp, and a downloadable high-resolution QR code receipt for voter verification.",
         "Voter",
         "Download receipt, print receipt, copy receipt hash"),
        ("Page 9 — Receipt Verification Desk",
         "A public verification desk allowing voters and auditors to input any receipt hash. The system queries the blockchain ledger and confirms whether the vote was mined into a valid block without exposing voter identity.",
         "All Roles",
         "Input receipt hash, query blockchain, view verification status"),
        ("Page 10 — Blockchain Explorer",
         "A full-page ledger browser displaying all mined blocks with block index, timestamp, previous hash, current hash, nonce, Merkle root, and transaction count. Includes a 1-click ledger audit button to detect chain tampering.",
         "All Roles",
         "Inspect block details, search transactions, trigger chain audit"),
        ("Page 11 — Observer Dashboard",
         "An analytics and transparency page for Observers and Admin. Displays summary cards — Total Registered Voters, Total Votes Cast, Voter Turnout Percentage, Leading Candidates. Interactive Recharts render real-time vote distribution.",
         "Observer, Admin",
         "View live stats, toggle chart visualizers, export CSV report"),
        ("Page 12 — AI Fraud Radar",
         "A security monitoring dashboard tracking vote velocity bursts (<2s), duplicate IP clusters, and double-voting attempts. Computes a composite Threat Index (0-100%) and categorizes election health.",
         "Admin, Observer",
         "View velocity graph, inspect flagged IP clusters, review threat score"),
    ]

    for p_title, p_desc, p_acc, p_int in pages_p7_12:
        story.append(Paragraph(f"<b>{p_title}</b>", h2_navy))
        story.append(Paragraph(p_desc, body))
        story.append(Paragraph(f"<b>Accessible By:</b> {p_acc}", body))
        story.append(Paragraph(f"<b>Interactions:</b> {p_int}", body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: 8. DATA REQUIREMENTS (8.1 ROLE, 8.2 USER, 8.3 ELECTION) (Page 13)
    # =========================================================================
    story.append(Paragraph("8. Data Requirements", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "All persistent data is stored in a relational database. Tables are normalised to Third Normal Form (3NF) to "
        "minimise redundancy. Foreign key constraints enforce referential integrity across all relationships.",
        body
    ))

    story.append(Paragraph("8.1 ROLE", h2))
    role_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("role_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("role_name", td), Paragraph("VARCHAR(50)", td), Paragraph("—", td), Paragraph("Admin, Voter, Observer", td)],
    ]
    t_r = Table(role_data, colWidths=[100, 90, 60, 250])
    t_r.setStyle(navy_table_style)
    story.append(t_r)

    story.append(Paragraph("8.2 USER", h2))
    user_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("user_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("name", td), Paragraph("VARCHAR(100)", td), Paragraph("—", td), Paragraph("Full name of the user", td)],
        [Paragraph("email", td), Paragraph("VARCHAR(100)", td), Paragraph("UNIQUE", td), Paragraph("Login credential and unique identifier", td)],
        [Paragraph("password", td), Paragraph("VARCHAR(255)", td), Paragraph("—", td), Paragraph("Hashed password (bcrypt)", td)],
        [Paragraph("role_id", td), Paragraph("INT", td), Paragraph("FK → ROLE", td), Paragraph("Defines the access role assigned to this user", td)],
        [Paragraph("is_active", td), Paragraph("BOOLEAN", td), Paragraph("—", td), Paragraph("Account status — active or deactivated", td)],
    ]
    t_u = Table(user_data, colWidths=[100, 90, 60, 250])
    t_u.setStyle(navy_table_style)
    story.append(t_u)

    story.append(Paragraph("8.3 ELECTION", h2))
    elec_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("election_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("title", td), Paragraph("VARCHAR(200)", td), Paragraph("—", td), Paragraph("Title of the election", td)],
        [Paragraph("description", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("Full election description and rules", td)],
        [Paragraph("status", td), Paragraph("VARCHAR(20)", td), Paragraph("—", td), Paragraph("Draft / Active / Closed", td)],
        [Paragraph("start_time", td), Paragraph("DATETIME", td), Paragraph("—", td), Paragraph("Scheduled election opening timestamp", td)],
        [Paragraph("end_time", td), Paragraph("DATETIME", td), Paragraph("—", td), Paragraph("Scheduled election closing timestamp", td)],
        [Paragraph("created_by", td), Paragraph("INT", td), Paragraph("FK → USER", td), Paragraph("Admin user who created the election", td)],
    ]
    t_e = Table(elec_data, colWidths=[100, 90, 60, 250])
    t_e.setStyle(navy_table_style)
    story.append(t_e)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: 8. DATA REQUIREMENTS (8.4 CANDIDATE, 8.5 VOTE, 8.6 BLOCK) (Page 14)
    # =========================================================================
    story.append(Paragraph("8.4 CANDIDATE", h2))
    cand_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("candidate_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("election_id", td), Paragraph("INT", td), Paragraph("FK → ELECTION", td), Paragraph("Election this candidate is running in", td)],
        [Paragraph("name", td), Paragraph("VARCHAR(100)", td), Paragraph("—", td), Paragraph("Full name of the candidate", td)],
        [Paragraph("party", td), Paragraph("VARCHAR(100)", td), Paragraph("—", td), Paragraph("Party name or organizational affiliation", td)],
        [Paragraph("manifesto", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("Candidate manifesto and platform promises", td)],
        [Paragraph("avatar_url", td), Paragraph("VARCHAR(255)", td), Paragraph("—", td), Paragraph("URL to candidate portrait image", td)],
        [Paragraph("vote_count", td), Paragraph("INT", td), Paragraph("—", td), Paragraph("Aggregated tally of confirmed votes", td)],
    ]
    t_c = Table(cand_data, colWidths=[100, 90, 60, 250])
    t_c.setStyle(navy_table_style)
    story.append(t_c)

    story.append(Paragraph("8.5 VOTE", h2))
    vote_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("vote_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("user_id", td), Paragraph("INT", td), Paragraph("FK → USER", td), Paragraph("Voter account who cast the ballot", td)],
        [Paragraph("election_id", td), Paragraph("INT", td), Paragraph("FK → ELECTION", td), Paragraph("Election being voted on", td)],
        [Paragraph("candidate_id", td), Paragraph("INT", td), Paragraph("FK → CANDIDATE", td), Paragraph("Selected candidate", td)],
        [Paragraph("voter_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("—", td), Paragraph("Anonymous SHA-256 voter fingerprint", td)],
        [Paragraph("encrypted_vote", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("AES-256 GCM encrypted ballot payload", td)],
        [Paragraph("tx_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("UNIQUE", td), Paragraph("Unique cryptographic transaction hash", td)],
        [Paragraph("block_index", td), Paragraph("INT", td), Paragraph("—", td), Paragraph("Index of the mined block containing the vote", td)],
        [Paragraph("receipt_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("UNIQUE", td), Paragraph("Verifiable receipt lookup hash", td)],
    ]
    t_v = Table(vote_data, colWidths=[100, 90, 60, 250])
    t_v.setStyle(navy_table_style)
    story.append(t_v)

    story.append(Paragraph("8.6 BLOCK", h2))
    blk_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("block_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("block_index", td), Paragraph("INT", td), Paragraph("UNIQUE", td), Paragraph("Sequential block index in chain (0 = Genesis)", td)],
        [Paragraph("timestamp", td), Paragraph("FLOAT", td), Paragraph("—", td), Paragraph("Unix timestamp when block was mined", td)],
        [Paragraph("previous_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("—", td), Paragraph("SHA-256 hash of the preceding block", td)],
        [Paragraph("hash", td), Paragraph("VARCHAR(64)", td), Paragraph("UNIQUE", td), Paragraph("SHA-256 hash of current block meeting PoW target", td)],
        [Paragraph("nonce", td), Paragraph("INT", td), Paragraph("—", td), Paragraph("Proof-of-Work counter satisfying difficulty", td)],
        [Paragraph("merkle_root", td), Paragraph("VARCHAR(64)", td), Paragraph("—", td), Paragraph("Binary Merkle root aggregating block transactions", td)],
        [Paragraph("signature", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("System ECDSA digital signature", td)],
    ]
    t_b = Table(blk_data, colWidths=[100, 90, 60, 250])
    t_b.setStyle(navy_table_style)
    story.append(t_b)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: 8. DATA REQUIREMENTS (8.7 TRANSACTION, 8.8 AI_ANOMALY, 8.9 AUDIT_LOG) (Page 15)
    # =========================================================================
    story.append(Paragraph("8.7 TRANSACTION", h2))
    tx_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("tx_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("tx_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("UNIQUE", td), Paragraph("SHA-256 transaction digest", td)],
        [Paragraph("block_index", td), Paragraph("INT", td), Paragraph("FK → BLOCK", td), Paragraph("Block that confirmed this transaction", td)],
        [Paragraph("election_id", td), Paragraph("INT", td), Paragraph("FK → ELECTION", td), Paragraph("Associated election ID", td)],
        [Paragraph("voter_hash", td), Paragraph("VARCHAR(64)", td), Paragraph("—", td), Paragraph("Anonymous voter hash", td)],
        [Paragraph("encrypted_vote", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("AES-256 encrypted payload", td)],
        [Paragraph("signature", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("Voter ECDSA digital signature", td)],
    ]
    t_tx = Table(tx_data, colWidths=[100, 90, 60, 250])
    t_tx.setStyle(navy_table_style)
    story.append(t_tx)

    story.append(Paragraph("8.8 AI_ANOMALY", h2))
    ai_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("anomaly_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("election_id", td), Paragraph("INT", td), Paragraph("FK → ELECTION", td), Paragraph("Associated election ID", td)],
        [Paragraph("anomaly_type", td), Paragraph("VARCHAR(50)", td), Paragraph("—", td), Paragraph("Velocity Spike / IP Cluster / Double Vote", td)],
        [Paragraph("ip_address", td), Paragraph("VARCHAR(45)", td), Paragraph("—", td), Paragraph("Client IP address flagged", td)],
        [Paragraph("risk_score", td), Paragraph("FLOAT", td), Paragraph("—", td), Paragraph("Computed threat score (0.0 to 100.0)", td)],
        [Paragraph("timestamp", td), Paragraph("DATETIME", td), Paragraph("—", td), Paragraph("Timestamp when anomaly was flagged", td)],
    ]
    t_ai = Table(ai_data, colWidths=[100, 90, 60, 250])
    t_ai.setStyle(navy_table_style)
    story.append(t_ai)

    story.append(Paragraph("8.9 AUDIT_LOG", h2))
    log_data = [
        [Paragraph("Field Name", th), Paragraph("Data Type", th), Paragraph("Key", th), Paragraph("Description", th)],
        [Paragraph("log_id", td), Paragraph("INT", td), Paragraph("PK", td), Paragraph("Auto-increment primary key", td)],
        [Paragraph("user_id", td), Paragraph("INT", td), Paragraph("FK → USER", td), Paragraph("User session being recorded", td)],
        [Paragraph("user_email", td), Paragraph("VARCHAR(100)", td), Paragraph("—", td), Paragraph("User email recorded at event time", td)],
        [Paragraph("action", td), Paragraph("VARCHAR(100)", td), Paragraph("—", td), Paragraph("Action performed (LOGIN, CAST_VOTE, CREATE_ELECTION)", td)],
        [Paragraph("details", td), Paragraph("TEXT", td), Paragraph("—", td), Paragraph("Contextual details and metadata", td)],
        [Paragraph("ip_address", td), Paragraph("VARCHAR(45)", td), Paragraph("—", td), Paragraph("Client IP address", td)],
        [Paragraph("timestamp", td), Paragraph("DATETIME", td), Paragraph("—", td), Paragraph("Event timestamp", td)],
    ]
    t_l = Table(log_data, colWidths=[100, 90, 60, 250])
    t_l.setStyle(navy_table_style)
    story.append(t_l)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: 8.10 ENTITY RELATIONSHIP SUMMARY (Page 16)
    # =========================================================================
    story.append(Paragraph("8.10 Entity Relationship Summary", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_NAVY, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("The relationships between core database entities are as follows:", body))

    er_points = [
        "● <b>ROLE (1) → USER (many):</b> Each user is assigned one role; a role may be assigned to many users.",
        "● <b>USER (1) → VOTE (many):</b> Each voter can cast votes across multiple distinct elections (enforcing a unique compound constraint on user_id, election_id).",
        "● <b>ELECTION (1) → CANDIDATE (many):</b> An election contains multiple running candidates.",
        "● <b>ELECTION (1) → VOTE (many):</b> An election accumulates confirmed votes from registered voters.",
        "● <b>ELECTION (1) → AI_ANOMALY (many):</b> An election generates real-time AI anomaly detection logs.",
        "● <b>BLOCK (1) → TRANSACTION (many):</b> A mined block contains multiple confirmed vote transactions.",
        "● <b>USER (1) → AUDIT_LOG (many):</b> Each user session generates immutable security audit log entries.",
    ]
    for ep in er_points:
        story.append(Paragraph(ep, bullet))

    # Build the exact 16-page PDF document
    doc.build(story)
    print(f"Successfully generated exact 16-page SRS PDF at: {filename}")

if __name__ == "__main__":
    generate_exact_16page_srs()
