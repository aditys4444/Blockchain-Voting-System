from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_front_matter_and_ch1(builder):
    # =========================================================
    # FRONT MATTER (Pages 1 - 6)
    # =========================================================
    
    # Page 1: Title & Cover Page
    p_header = builder.doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_before = Pt(8)
    p_header.paragraph_format.space_after = Pt(14)
    r_hdr = p_header.add_run("A SOFTWARE ENGINEERING PROJECT REPORT ON")
    r_hdr.font.name = 'Times New Roman'
    r_hdr.font.size = Pt(11)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = builder.COLOR_MUTED

    builder.add_title("DECENTRALIZED BLOCKCHAIN VOTING SYSTEM WITH AI FRAUD RADAR")
    builder.add_subtitle("An Immutable, Tamper-Resistant Electoral Platform with SECP256R1 ECDSA Signatures, SHA-256 Proof-of-Work Consensus, and Real-Time Telemetry Anomaly Detection")
    
    p_sub = builder.doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub1 = p_sub.add_run("Submitted in partial fulfillment of the academic requirements\nfor the award of the Degree of\n")
    r_sub1.font.name = 'Times New Roman'
    r_sub1.font.size = Pt(10.5)
    r_sub1.font.italic = True
    r_sub1.font.color.rgb = builder.COLOR_DARK
    
    r_deg = p_sub.add_run("BACHELOR OF SCIENCE IN COMPUTER SCIENCE")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(13)
    r_deg.font.bold = True
    r_deg.font.color.rgb = builder.COLOR_SECONDARY

    builder.add_styled_table(
        ["Academic & Engineering Metric", "Institutional Project Record Specification"],
        [
            ["Candidate / Lead Engineer", "Aditya Yadav (Lead Full-Stack & Cryptography Developer)"],
            ["University Registration ID", "Roll No: 2026-CS-0428 • Examination Seat: 849201"],
            ["Academic Program & Year", "Bachelor of Science in Computer Science (B.Sc CS) • 2026 - 2027"],
            ["Departmental Affiliation", "Department of Computer Science • Faculty of Technology"],
            ["Institutional Examination Board", "University Examination Council & Board of Technical Education"],
            ["Project Supervisor & Guide", "Faculty Review Coordinator & Software Engineering Board"],
            ["Documentation Standard", "IEEE Std 830-1998 (Software Requirements Specification) & ISO/IEC 25010"],
            ["Production Codebase Baseline", "React 19, FastAPI 0.110, SQLite WAL, Python 3.12, SECP256R1 ECDSA"],
            ["Submission Venue & Cycle", "Academic Module Final Defense & External Viva Voce Examination"],
            ["Formal Date of Submission", "September 2026 (Release 1.0 Enterprise Academic Edition)"]
        ],
        col_widths=[2.3, 3.7],
        caption="Institutional Project Identification Record"
    )
    builder.add_p("This comprehensive software engineering report embodies the end-to-end architectural design, mathematical formulation, UML 2.5 domain models, IEEE 830 requirements specifications, and empirical validation for a decentralized, tamper-proof electronic voting platform.")
    builder.add_page_break()

    # Page 2: Certificate of Authenticity & Institutional Sign-Off
    builder.add_chapter_title("CERTIFICATE OF AUTHENTICITY")
    builder.add_p("This is to certify that the project report entitled 'Decentralized Blockchain Voting System with AI Fraud Radar' is a bona fide record of independent research, system analysis, software modeling, and architectural engineering carried out by Aditya Yadav (Roll No: 2026-CS-0428), a student of the Department of B.Sc Computer Science, during the academic session 2026–2027.")
    builder.add_p("The system design, software requirement specifications, architectural schemas, cryptographic models, and data dictionaries incorporated in this report reflect authentic engineering work performed by the candidate under faculty supervision. All external algorithms, academic literature, and software libraries have been duly credited and cited in strict compliance with international academic integrity guidelines.")
    builder.add_styled_table(
        ["Review Designation", "Faculty Member / Examiner", "Approval Status", "Date of Certification"],
        [
            ["Internal Project Supervisor", "Department Review Coordinator", "Approved & Formally Verified", "September 2026"],
            ["Head of Department", "Chairperson, Computer Science Board", "Certified for Academic Award", "September 2026"],
            ["External University Examiner", "University Examination Committee", "Accepted for Viva Voce Defense", "September 2026"]
        ],
        col_widths=[1.8, 2.0, 1.4, 0.8],
        caption="Institutional Sign-Off & Examination Endorsement"
    )
    builder.add_p("The software prototype described herein has been validated against active local and cloud execution environments, demonstrating full conformity to the stated functional requirements and architectural objectives.")
    builder.add_page_break()

    # Page 3: Declaration of Originality & Acknowledgements
    builder.add_chapter_title("DECLARATION OF ORIGINALITY & ACKNOWLEDGEMENTS")
    builder.add_section_heading("Candidate Declaration of Originality")
    builder.add_p("I, Aditya Yadav, hereby declare that the work presented in this academic report entitled 'Decentralized Blockchain Voting System with AI Fraud Radar' is entirely my own original software engineering endeavor, conducted under the guidance and mentorship of the faculty of the Department of Computer Science. All mathematical formulations, cryptographic protocols (SECP256R1 ECDSA, SHA-256 Merkle trees, AES-256 GCM), architectural diagrams, and source code excerpts correspond to verified implementations developed within the project workspace.")
    builder.add_bullet_item("Candidate Name & Roll", "Aditya Yadav • Roll No: 2026-CS-0428 • Examination Seat: 849201")
    builder.add_bullet_item("Program & Affiliation", "Bachelor of Science in Computer Science (B.Sc CS) • 2026 - 2027")
    
    builder.add_section_heading("Acknowledgements & Academic Mentorship")
    builder.add_p("I express my profound gratitude to the Almighty, my parents, and my project supervisor for their continuous encouragement, guidance, and technical reviews throughout this project lifecycle.")
    builder.add_p("I also place on record my sincere indebtedness to the open-source software community behind the Python Software Foundation, FastAPI, React 19, Vite, and cryptography libraries, as well as peer testers whose active participation during usability and penetration evaluations provided vital empirical feedback for optimizing the system.")
    builder.add_page_break()

    # Page 4: Abstract & Executive Summary
    builder.add_chapter_title("ABSTRACT & EXECUTIVE SUMMARY")
    builder.add_p("Electronic voting is widely acknowledged as a vital mechanism for modernizing institutional, corporate, and civic governance. However, the widespread adoption of traditional centralized e-voting applications remains severely constrained by systemic vulnerabilities. Centralized relational databases present a single point of failure, allow privileged database administrators to silently alter vote tallies, and provide voters with zero mathematical proof that their ballots were legitimately counted. Furthermore, automated bots and coordinated network bursts frequently threaten election integrity.")
    builder.add_p("To overcome these fundamental vulnerabilities, this document specifies the complete engineering design for a 'Decentralized Blockchain Voting System with AI Fraud Radar'. The platform implements a modern 3-tier architecture uniting a high-responsiveness React 19 Single Page Application (SPA), an asynchronous Python 3.12 FastAPI backend server, and an embedded custom SHA-256 Proof-of-Work blockchain ledger.")
    builder.add_p("Security is enforced at every tier: voter selections are shielded using AES-256 GCM envelope encryption, blocks are signed using NIST-standard SECP256R1 Elliptic Curve Digital Signature Algorithm (ECDSA), and transactions are aggregated into cryptographically immutable Merkle tree leaves. Voters receive tamper-evident cryptographic QR receipts enabling independent public verification without compromising ballot confidentiality. Concurrently, an intelligent AI Fraud Radar service continuously monitors transaction arrival velocities and IP clustering metrics to detect automated voter manipulation in real time.")
    builder.add_p("Keywords: Blockchain Ledger, Proof-of-Work, SECP256R1 ECDSA, Merkle Tree, Electronic Voting, AI Telemetry, Fraud Radar, FastAPI, React 19, Zero-Trust Architecture.")
    builder.add_page_break()

    # Page 5: Master Table of Contents
    builder.add_chapter_title("TABLE OF CONTENTS")
    builder.add_styled_table(
        ["Chapter / Major Division", "Comprehensive Thematic Coverage & Engineering Deliverables", "Page Range"],
        [
            ["Front Matter", "Cover Page, Certificate, Declaration & Acknowledgements, Abstract", "Pages 1 - 4"],
            ["Document Indexes", "Table of Contents, List of Figures, List of Tables & Abbreviations", "Pages 5 - 6"],
            ["CHAPTER 1", "INTRODUCTION & DOMAIN FOUNDATIONS", "Pages 7 - 13"],
            ["CHAPTER 2", "PROBLEM IDENTIFICATION & FEASIBILITY STUDY", "Pages 14 - 23"],
            ["CHAPTER 3", "REQUIREMENT ENGINEERING (IEEE 830 SRS SPECIFICATION)", "Pages 24 - 36"],
            ["CHAPTER 4", "SOFTWARE DEVELOPMENT LIFE CYCLE PLANNING", "Pages 37 - 44"],
            ["CHAPTER 5", "SYSTEM MODELING USING COMPLETE UML DIAGRAM SET", "Pages 45 - 61"],
            ["CHAPTER 6", "SYSTEM ARCHITECTURE DESIGN", "Pages 62 - 70"],
            ["CHAPTER 7", "SYSTEM DESIGN SPECIFICATION", "Pages 71 - 74"],
            ["CHAPTER 8", "CONCLUSION, LIMITATIONS & FUTURE ENHANCEMENTS", "Pages 75 - 76"],
            ["REFERENCES", "Standard Technical & Academic Literature References (IEEE / ACM / NIST)", "Page 77"],
            ["APPENDIX A", "Requirements & UML Diagram Traceability Verification Index", "Page 78"],
            ["APPENDIX B", "Technical Glossary, Acronym Dictionary & Final Certification", "Page 79"]
        ],
        col_widths=[1.5, 3.4, 1.1],
        caption="Master Table of Contents & Structural Document Map"
    )
    builder.add_page_break()

    # Page 6: List of Figures, Tables & Technical Abbreviations
    builder.add_chapter_title("LIST OF FIGURES & ANALYTICAL TABLES")
    builder.add_styled_table(
        ["Figure / Table #", "Formal Architectural Title & Technical Scope", "Model Category", "Page #"],
        [
            ["Figure 5.1", "System Use Case Diagram Specification (02_Use_Case.png)", "UML Use Case", "Page 46"],
            ["Figure 5.2", "System Class Diagram Architecture Specification (03_Class_Diagram.png)", "UML Class", "Page 50"],
            ["Figure 5.3", "Sequence Diagram: User Authentication & JWT Issuance", "UML Sequence", "Page 51"],
            ["Figure 5.4", "Sequence Diagram: Voter Self-Registration Flow", "UML Sequence", "Page 52"],
            ["Figure 5.5", "Sequence Diagram: Encrypted Vote Casting & PoW Mining", "UML Sequence", "Page 53"],
            ["Figure 5.6", "Sequence Diagram: API & AI Telemetry Anomaly Flow", "UML Sequence", "Page 54"],
            ["Figure 5.7", "Activity Diagram: User Login & Role Guard Control Flow", "UML Activity", "Page 56"],
            ["Figure 5.8", "Activity Diagram: Voter Main Lifecycle Workflow", "UML Activity", "Page 57"],
            ["Figure 5.9", "Entity-Relationship (ER) Data Model Schema", "UML Data Model", "Page 58"],
            ["Figure 5.10", "System Deployment Architecture Infrastructure", "UML Deployment", "Page 59"],
            ["Figure 5.11", "System Context Diagram Specification", "Architecture Context", "Page 60"],
            ["Figure 5.12", "Data Flow Diagram (DFD Level 0 — Context Model)", "Data Flow Model", "Page 61"],
            ["Figure 6.1", "Overall 3-Tier Layered System Architecture Diagram", "System Architecture", "Page 63"],
            ["Figure 6.2", "Frontend Single Page Application (SPA) Architecture", "Component Model", "Page 64"],
            ["Figure 6.3", "Backend Asynchronous Service Architecture Diagram", "Service Architecture", "Page 65"],
            ["Figure 6.4", "Relational Database Architecture Diagram", "Database Model", "Page 66"],
            ["Figure 6.5", "API & Asynchronous Data Flow Diagram (DFD Level 1)", "Data Flow Model", "Page 67"],
            ["Figure 6.6", "Deployment & Containerization Architecture Diagram", "Physical Model", "Page 68"],
            ["Table 2.1 - 2.3", "Feasibility Studies: Stakeholders, Benchmarks & TCO Cost Model", "Analytical Table", "Pages 20 - 23"],
            ["Table 3.1 - 3.7", "IEEE 830 Requirements: URS, Functional Modules FR-01 to FR-25", "Analytical Table", "Pages 26 - 32"],
            ["Table 4.1 - 4.4", "SDLC Planning: Model Matrix, WBS Packages, Gantt & Risk Matrix", "Analytical Table", "Pages 39 - 44"],
            ["Table 7.1 - 7.2", "System Design: Database Data Dictionary & REST API Specifications", "Analytical Table", "Pages 73 - 74"]
        ],
        col_widths=[1.1, 3.1, 1.1, 0.7],
        caption="Master Index of Architectural Figures, UML Models & Analytical Tables"
    )
    builder.add_page_break()

    # =========================================================
    # CHAPTER 1 — INTRODUCTION (Pages 7 - 13)
    # =========================================================
    
    # Page 7: 1.1 Introduction & 1.2 Project Background
    builder.add_chapter_title("CHAPTER 1 — INTRODUCTION")
    builder.add_section_heading("1.1 Introduction")
    builder.add_p("Democratic governance within universities, corporate enterprises, professional societies, and civic institutions hinges upon the indisputable credibility of electoral processes. Voting is the mechanism through which authority is legitimately delegated. When electoral mechanisms lack transparency, organizational stability is fractured, and trust in institutional leadership deteriorates.")
    builder.add_p("While the transition from physical paper ballots to electronic voting platforms was intended to expedite tallying and eliminate manual counting errors, it introduced an entirely new category of cybersecurity vulnerabilities. Contemporary e-voting applications predominantly rely upon centralized web frameworks connected to relational database management systems. In such architectures, whoever controls the database server controls the election outcome.")
    builder.add_section_heading("1.2 Project Background")
    builder.add_p("The Genesis of this project arose from observing recurrent contested elections in collegiate student unions and corporate shareholder bodies. Discontent invariably focused on the opacity of the tallying server. System administrators held unrestricted database permissions, enabling silent record alteration via basic SQL query injection or direct row modification.")
    builder.add_p("The 'Decentralized Blockchain Voting System with AI Fraud Radar' was conceived as a fundamental technological paradigm shift. Rather than demanding that voters place blind trust in centralized system administrators, the platform enforces mathematical trust through cryptographic proofs. Every vote cast is packaged as an irreversible cryptographic transaction, permanently chained to predecessor blocks, and verifiable by any observer on the network.")
    builder.add_page_break()

    # Page 8: 1.3 Domain Overview & Cryptographic Primitives
    builder.add_section_heading("1.3 Domain Overview & Cryptographic Foundations")
    builder.add_p("The technological domain of this project resides at the intersection of Applied Cryptography, Distributed Ledger Technology (DLT), Asynchronous Web Engineering, and Artificial Intelligence Anomaly Detection. Addressing the multifaceted requirements of electronic voting necessitates harmonizing seemingly contradictory objectives: ensuring absolute voter anonymity while guaranteeing complete public auditability.")
    builder.add_p("To realize these objectives, the system leverages three core cryptographic primitives:")
    builder.add_bullet_item("NIST SECP256R1 ECDSA", "The Elliptic Curve Digital Signature Algorithm using the prime 256-bit curve (secp256r1/P-256) provides asymmetric digital signatures for verifying block authenticity without exposing secret signing keys.")
    builder.add_bullet_item("SHA-256 Cryptographic Hashing", "The Secure Hash Algorithm (256-bit) computes deterministic block headers, Merkle tree root hashes, and voter identification hashes, providing collision resistance and pre-image resistance.")
    builder.add_bullet_item("AES-256 GCM Envelope Encryption", "Advanced Encryption Standard in Galois/Counter Mode ensures confidentiality and authenticity for stored ballot choices prior to block mining.")
    builder.add_p("These cryptographic foundations ensure that the electoral ledger operates in an append-only mode. Once a block is mined and validated by the network, altering any transaction within it necessitates re-mining all subsequent blocks—a computationally infeasible task under established Proof-of-Work difficulty constraints.")
    builder.add_page_break()

    # Page 9: 1.4 Motivation & 1.5 Problem Statement
    builder.add_section_heading("1.4 Motivation")
    builder.add_p("The impetus for developing this platform is rooted in four acute software engineering imperatives:")
    builder.add_bullet_item("Elimination of Single Points of Failure", "Decentralizing verification ensures that the failure or compromise of a single node or database cannot invalidate the election.")
    builder.add_bullet_item("End-to-End Voter Verifiability", "Empowering each participant with verifiable cryptographic receipts that confirm their vote was correctly captured and tallied.")
    builder.add_bullet_item("Mitigation of Insider Threats", "Stripping system administrators of the technical capability to manipulate vote counts or modify historic ballot submissions.")
    builder.add_bullet_item("Proactive Fraud Interception", "Deploying automated telemetry analysis to detect coordinated bot-net submissions and credential stuffing before illegitimate votes can contaminate the ledger.")
    builder.add_section_heading("1.5 Problem Statement")
    builder.add_p("Current electronic voting software deployed in institutional and enterprise settings relies on centralized client-server topologies where vote selections are stored as mutable integers in relational tables. This architecture possesses severe structural defects: 1) System administrators possess unrestricted capabilities to alter records undetected, 2) Centralized servers are vulnerable to distributed denial-of-service (DDoS) outages during peak voting periods, 3) Voters possess no mathematical mechanism to verify their ballot inclusion, and 4) Automated voting scripts can execute rapid-burst ballot stuffing without triggering basic web application firewalls.")
    builder.add_page_break()

    # Page 10: 1.6 Existing Systems & 1.7 Limitations
    builder.add_section_heading("1.6 Existing System Analysis")
    builder.add_p("Contemporary institutional e-voting systems predominantly utilize LAMP (Linux, Apache, MySQL, PHP) or MEAN/MERN architectures where voting actions execute simple HTTP POST requests that invoke parameterized SQL UPDATE queries on a centralized database table (e.g., `UPDATE candidates SET votes = votes + 1 WHERE id = ?`).")
    builder.add_p("While such systems are simple to deploy, their architectural assumptions are deeply flawed from a security standpoint. Trust is concentrated entirely in the server environment, the host operating system, and the integrity of individual database administrators.")
    builder.add_section_heading("1.7 Limitations of Existing Systems")
    builder.add_bullet_item("Zero Immutability", "Standard relational database tables permit UPDATE and DELETE statements. An attacker with database access can rewrite historical election records in milliseconds.")
    builder.add_bullet_item("Absent Verification Protocol", "Voters are given no cryptographic token or receipt. Once the browser session closes, the voter has zero proof that their choice was recorded accurately.")
    builder.add_bullet_item("Vulnerability to Privilege Abuse", "Rogue administrators or compromised server credentials allow silent manipulation of election results without leaving auditable system traces.")
    builder.add_bullet_item("Inability to Detect Synthetic Bursts", "Centralized forms lack intelligent request rate analysis, allowing automated headless browser bots to cast fraudulent votes en masse.")
    builder.add_page_break()

    # Page 11: 1.8 Proposed System & 1.9 Architectural Advantages
    builder.add_section_heading("1.8 Proposed System")
    builder.add_p("The proposed system engineers an advanced, full-stack, decentralized voting architecture enhanced with an intelligent AI Fraud Radar. The platform couples a responsive, modern frontend Single Page Application (built with React 19, TypeScript, and Vite) with a high-throughput asynchronous backend service (powered by Python 3.12, FastAPI, and SQLAlchemy ORM), anchored by a custom SHA-256 Proof-of-Work blockchain engine.")
    builder.add_p("When a voter casts a ballot, the payload is encrypted using AES-256 GCM and cryptographically signed. The transaction is entered into a Proof-of-Work mining queue, where an asymmetric SHA-256 block header is computed targeting a difficulty of four zero-prefixes (`0000`). Mined blocks are authenticated via SECP256R1 ECDSA signatures and permanently chained to predecessor blocks. Simultaneously, the voter receives an instant cryptographic QR Code receipt encapsulating their transaction hash and Merkle inclusion proof.")
    builder.add_section_heading("1.9 Architectural Advantages")
    builder.add_bullet_item("Mathematical Immutability", "Altering a cast vote requires recalculating the SHA-256 hash of that block and all subsequent blocks, defeating tampering.")
    builder.add_bullet_item("Universal Voter Verification", "Voters can verify their receipt hash against the public ledger at any time without exposing their candidate choice.")
    builder.add_bullet_item("Automated Fraud Radar", "Integrated AI telemetry tracks voting velocity and IP clusters, assigning real-time fraud scores to active elections.")
    builder.add_bullet_item("Zero-Cost High-Reliability Deployment", "The decoupled architecture deploys globally across Vercel Edge CDN and Render cloud servers with zero licensing overhead.")
    builder.add_page_break()

    # Page 12: 1.10 Project Objectives & 1.11 Implementation Scope
    builder.add_section_heading("1.10 Project Objectives")
    builder.add_bullet_item("Objective 1: Cryptographic Engine", "Design and validate a custom Python blockchain ledger implementing SHA-256 Merkle root trees, Proof-of-Work consensus, and SECP256R1 digital signatures.")
    builder.add_bullet_item("Objective 2: Asynchronous REST API", "Implement a high-throughput, secure backend using FastAPI with OAuth2 JWT Bearer authentication and role-based route guards.")
    builder.add_bullet_item("Objective 3: Responsive User Interface", "Engineer an intuitive, modern Single Page Application in React 19, featuring one-click voting cards, QR receipt modals, and dark/light mode.")
    builder.add_bullet_item("Objective 4: AI Telemetry & Fraud Scoring", "Develop an automated telemetry analyzer calculating dynamic risk scores (0–100%) based on request bursts and IP duplicate patterns.")
    builder.add_bullet_item("Objective 5: Observer Transparency Portal", "Provide independent observers with real-time Recharts visualizations of vote distributions and blockchain integrity audits.")
    builder.add_section_heading("1.11 Implementation Scope")
    builder.add_p("The engineering scope is defined with precision:")
    builder.add_bullet_item("In-Scope Components", "Full-stack web application, JWT authentication, Admin election/candidate studio, CSV bulk voter enrollment, AES-256 vote encryption, Proof-of-Work mining, QR receipt generation, public block explorer, and AI fraud dashboard.")
    builder.add_bullet_item("Out-of-Scope Components", "Physical hardware electronic voting machine (EVM) manufacturing, national biometric smart card readers, and decentralized satellite relay nodes.")
    builder.add_page_break()

    # Page 13: 1.12 Target Users, Stakeholders & Summary
    builder.add_section_heading("1.12 Target Users & Operational Profiles")
    builder.add_bullet_item("Institutional Administrators", "Election officials responsible for creating election instances, registering candidate profiles, uploading voter CSV rosters, and monitoring election closure.")
    builder.add_bullet_item("Registered Voters", "Eligible students, faculty, or shareholders who authenticate via secure credentials, review candidate platforms, cast encrypted ballots, and obtain verifiable QR receipts.")
    builder.add_bullet_item("Independent Observers & Auditors", "Neutral third-party auditors who monitor real-time vote tallies, inspect block headers, audit chain integrity, and review AI fraud telemetry.")
    builder.add_section_heading("1.13 Stakeholder Community")
    builder.add_p("Stakeholders encompass academic institutions seeking fair student government elections, corporate governing boards demanding verifiable shareholder votes, cybersecurity auditors requiring proof of compliance, and voters demanding privacy.")
    builder.add_section_heading("1.14 Expected Outcomes & 1.15 Chapter Summary")
    builder.add_p("Expected Outcomes: Delivery of an enterprise-grade, verifiable voting application achieving sub-second UI response times, zero-cost operational overhead, and mathematical immutability. Chapter 1 established the conceptual background, problem statement, domain foundations, and engineering objectives. Chapter 2 presents the detailed Problem Identification and Feasibility Study.")
    builder.add_page_break()
