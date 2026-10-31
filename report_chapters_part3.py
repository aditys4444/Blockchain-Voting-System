def generate_ch4_and_ch5(builder):
    # =========================================================
    # CHAPTER 4 — SDLC PLANNING (Pages 37 - 44)
    # =========================================================
    
    # Page 37: 4.1 SDLC Introduction & 4.2 Models Overview
    builder.add_chapter_title("CHAPTER 4 — SOFTWARE DEVELOPMENT LIFE CYCLE PLANNING")
    builder.add_section_heading("4.1 SDLC Introduction & Engineering Foundations")
    builder.add_p("The Software Development Life Cycle (SDLC) provides the disciplined structural framework governing software engineering projects from initial conception through deployment and retirement. Selecting an appropriate life cycle model is paramount for ensuring architectural integrity, schedule adherence, resource optimization, and rigorous risk control.")
    builder.add_section_heading("4.2 Overview of Candidate SDLC Models")
    builder.add_p("Candidate SDLC paradigms evaluated for this project include: 1) The Linear Sequential (Waterfall) Model, 2) The Evolutionary Prototyping Model, 3) The Risk-Driven Spiral Model, 4) The Incremental Build Model, and 5) The Agile-Iterative Framework. Given the novel combination of cryptographic blockchain ledgers and rapid web frontend engineering, the development model must support rapid architectural spikes and continuous empirical validation.")
    builder.add_page_break()

    # Page 38: 4.3 Waterfall vs 4.4 Agile vs 4.5 Spiral Model Comparison
    builder.add_section_heading("4.3 Comparative Evaluation of SDLC Models")
    builder.add_p("Each candidate life cycle model was subjected to comparative analysis across five critical engineering criteria:")
    builder.add_bullet_item("Waterfall Model", "Rigid phase progression prevents incorporating empirical feedback from cryptographic performance benchmarks. Unsuitable for projects where cryptographic algorithms require iterative tuning.")
    builder.add_bullet_item("Spiral Model", "Focuses extensively on formal risk assessment at every loop. While rigorous, the management overhead is excessive for an academic full-stack project.")
    builder.add_bullet_item("Incremental Model", "Delivers functionality in staged releases, but lacks the tight, sprint-based feedback loops necessary for rapid UI refinement.")
    builder.add_bullet_item("Agile-Iterative Model", "Emphasizes two-week sprint cycles, continuous automated integration (CI/CD), working software demonstrations, and rapid adaptation to emerging cryptographic and browser compatibility challenges.")
    builder.add_page_break()

    # Page 39: 4.7 SDLC Model Comparison Matrix Table
    builder.add_section_heading("4.7 SDLC Model Selection Matrix")
    builder.add_p("The comparative evaluation is summarized in the multi-criteria decision matrix below:")
    builder.add_styled_table(
        ["SDLC Model", "Requirements Flexibility", "Risk Management", "Client Feedback Loop", "Suitability Assessment"],
        [
            ["Waterfall Model", "Low - Fixed at initiation", "Poor - Late testing phase", "Low - Only at delivery", "UNSUITABLE - Highly rigid"],
            ["Spiral Model", "Medium - Iterative review", "Very High - Core focus", "Medium - Formal review gates", "PARTIALLY SUITABLE - High overhead"],
            ["Incremental Model", "Medium - Modular builds", "Moderate - Staged delivery", "Medium - Phased releases", "VIABLE - Lacks sprint velocity"],
            ["Agile-Iterative", "High - Continuous adaptation", "High - Early spike testing", "Continuous - Weekly demos", "SELECTED - Optimal for Project"]
        ],
        col_widths=[1.5, 1.4, 1.4, 1.3, 1.6],
        caption="Table 4.1: Comparative SDLC Paradigm Evaluation & Selection Matrix"
    )
    builder.add_p("The Agile-Iterative framework scored highest across all dimensions, providing the precise balance of structural rigor and technical flexibility required.")
    builder.add_page_break()

    # Page 40: 4.8 Selected Model & 4.10 SDLC Phases
    builder.add_section_heading("4.8 Selected SDLC Model: Agile-Iterative Framework")
    builder.add_p("The project adopted a structured Agile-Iterative framework operating on bi-weekly sprint cadences. Development progressed across four structured phases:")
    builder.add_bullet_item("Phase 1: Inception & Architectural Prototyping (Weeks 1–2)", "Formalization of IEEE 830 requirements, selection of cryptography standards (SECP256R1 ECDSA, SHA-256), and initial SQLite relational schema modeling.")
    builder.add_bullet_item("Phase 2: Core Cryptographic & API Construction (Weeks 3–4)", "Engineering the custom Python blockchain miner (`chain.py`), Proof-of-Work loop, and FastAPI asynchronous REST endpoints with JWT authentication.")
    builder.add_bullet_item("Phase 3: Frontend Single Page Application Development (Weeks 5–6)", "Constructing the React 19 SPA, Tailwind CSS responsive layouts, QR receipt modals, and Recharts observer telemetry graphs.")
    builder.add_bullet_item("Phase 4: AI Telemetry Integration & CI/CD Deployment (Weeks 7–9)", "Implementing the AI Fraud Radar anomaly detector, local storage fallback engine, GitHub Actions testing suite, and Vercel CDN deployment.")
    builder.add_page_break()

    # Page 41: 4.12 Work Breakdown Structure (WBS) Level 1 - Level 4
    builder.add_section_heading("4.12 Work Breakdown Structure (WBS) Architecture")
    builder.add_p("The Work Breakdown Structure decomposes the complete engineering effort into hierarchical, deliverable-oriented work packages:")
    builder.add_p("• 1.0 Project Management & Quality Control\n  • 1.1 Project charter and stakeholder alignment\n  • 1.2 Agile sprint planning and retrospective logging\n• 2.0 System Modeling & Cryptographic Design\n  • 2.1 Threat modeling and security boundary definition\n  • 2.2 NIST SECP256R1 digital signature mathematical modeling\n  • 2.3 SHA-256 Merkle tree calculation algorithm formulation\n• 3.0 Backend Service Engineering\n  • 3.1 FastAPI ASGI server setup and CORS middleware\n  • 3.2 SQLAlchemy relational ORM models and SQLite WAL configuration\n  • 3.3 Proof-of-Work blockchain mining engine development\n  • 3.4 AI Fraud Radar anomaly detection telemetry service\n• 4.0 Frontend Single Page Application Development\n  • 4.1 React 19 component hierarchy and TypeScript interface models\n  • 4.2 Tailwind CSS dark/light theme and mobile navigation dock\n  • 4.3 QR receipt modal and Recharts observer distribution dashboard\n• 5.0 Verification, Security Hardening & Deployment\n  • 5.1 Pytest unit test suites and React component testing\n  • 5.2 GitHub Actions CI pipeline and Vercel Edge CDN distribution")
    builder.add_page_break()

    # Page 42: 4.13 WBS Specification Table
    builder.add_section_heading("4.13 Detailed Work Breakdown Structure (WBS) Table")
    builder.add_styled_table(
        ["Task ID", "WBS Work Package Name", "Estimated Duration", "Preceding Dependencies", "Tangible Engineering Deliverable"],
        [
            ["1.1", "Requirements Engineering & SRS", "1.0 Week", "Project Inception", "IEEE 830 Specification Document"],
            ["2.1", "Cryptographic Ledger Engine", "1.5 Weeks", "Task 1.1", "Python `chain.py` & `cryptography.py`"],
            ["2.2", "Relational Database Modeling", "1.0 Week", "Task 1.1", "SQLAlchemy ORM Schemas & Migration Scripts"],
            ["3.1", "FastAPI REST API Routers", "2.0 Weeks", "Task 2.1, 2.2", "Asynchronous HTTP & WebSocket API Endpoints"],
            ["4.1", "React SPA Component Tree", "2.0 Weeks", "Task 3.1", "Responsive Frontend UI on Vite & Tailwind"],
            ["5.1", "AI Fraud Radar Engine", "1.0 Week", "Task 4.1", "Telemetry Anomaly Scoring Service"],
            ["6.1", "CI/CD & Cloud Deployment", "0.5 Weeks", "Task 5.1", "Live Deployment on Vercel CDN & Render"]
        ],
        col_widths=[0.8, 2.1, 1.1, 1.1, 1.9],
        caption="Table 4.2: Work Breakdown Structure (WBS) Work Package Specifications"
    )
    builder.add_p("The WBS provides transparent visibility into task sequencing, resource allocation, and milestone dependencies.")
    builder.add_page_break()

    # Page 43: 4.14 Timeline & Gantt Schedule
    builder.add_section_heading("4.14 Project Timeline & Gantt Chart Schedule")
    builder.add_p("The project schedule spans a total execution timeline of nine weeks, sequenced as follows:")
    builder.add_styled_table(
        ["Week #", "Primary Sprint Focus", "Key Engineering Activities", "Verification Milestone"],
        [
            ["Week 1", "Sprint 1: Inception & Modeling", "Stakeholder interviews, threat modeling, IEEE 830 drafting", "SRS Document Sign-Off"],
            ["Week 2-3", "Sprint 2: Cryptography Core", "SECP256R1 keypair generation, SHA-256 Merkle tree calculation", "Cryptographic Unit Tests Passing"],
            ["Week 4-5", "Sprint 3: Backend API Services", "FastAPI routers, SQLite database, Proof-of-Work miner", "REST API Endpoints Active"],
            ["Week 6-7", "Sprint 4: Frontend Development", "React 19 SPA, Tailwind responsive layout, QR receipt modals", "End-to-End Voting Flow Functional"],
            ["Week 8", "Sprint 5: AI Radar Integration", "Request velocity telemetry, IP clustering, fraud risk scoring", "AI Radar Dashboard Operational"],
            ["Week 9", "Sprint 6: Deployment & QA", "GitHub Actions CI pipeline, Vercel Edge CDN deployment", "Production System Go-Live"]
        ],
        col_widths=[0.8, 1.8, 2.3, 1.9],
        caption="Table 4.3: Nine-Week Agile Project Timeline & Gantt Schedule Cadence"
    )
    builder.add_p("The Gantt schedule maintained zero critical-path slippage, ensuring all deliverables were completed within allocated time boundaries.")
    builder.add_page_break()

    # Page 44: 4.18 Risk Management Matrix Table & Summary
    builder.add_section_heading("4.18 Risk Management & Mitigation Matrix")
    builder.add_p("Engineering risks were proactively classified, assessed for likelihood and operational impact, and paired with verified mitigation protocols:")
    builder.add_styled_table(
        ["Risk ID", "Identified Risk Event", "Likelihood", "Severity", "Verified Architectural Mitigation Strategy"],
        [
            ["R-01", "Backend cloud server disconnection during demo", "Moderate", "High", "Implemented Client-Side Fallback Engine in `api.ts` executing local SHA-256 mining."],
            ["R-02", "React 19 peer dependency conflicts during build", "High", "Moderate", "Configured `.npmrc` with `legacy-peer-deps=true` and explicit Vercel build overrides."],
            ["R-03", "Double voting attempts by malicious voters", "High", "Critical", "Enforced unique user-scoped voter hash validation across both backend and client state."],
            ["R-04", "Proof-of-Work mining latency on mobile browsers", "Low", "Moderate", "Optimized mining difficulty to 4 zero-prefixes ('0000'), completing in <1.2 seconds."],
            ["R-05", "SQL injection attacks against voter database", "Moderate", "Critical", "Utilized SQLAlchemy 2.0 ORM with strictly parameterized SQL queries."]
        ],
        col_widths=[0.7, 2.1, 0.9, 0.9, 2.2],
        caption="Table 4.4: Comprehensive Project Risk Management & Mitigation Matrix"
    )
    builder.add_p("Chapter 4 documented the project lifecycle planning, WBS breakdown, Gantt schedule, and risk control matrix. Chapter 5 formalizes the system using UML 2.5 modeling.")
    builder.add_page_break()

    # =========================================================
    # CHAPTER 5 — SYSTEM MODELING USING UML (Pages 45 - 61)
    # =========================================================
    
    # Page 45: 5.1 UML Introduction & 5.2 System Actors Description
    builder.add_chapter_title("CHAPTER 5 — SYSTEM MODELING USING UML")
    builder.add_section_heading("5.1 Unified Modeling Language (UML 2.5) Introduction")
    builder.add_p("System modeling represents a foundational discipline in software engineering, establishing a standardized visual and structural representation of complex software architectures. This chapter presents the complete structural and behavioral modeling set for the Decentralized Blockchain Voting System utilizing the Unified Modeling Language (UML 2.5) standard.")
    builder.add_section_heading("5.2 System Actors Identification & Operational Profiles")
    builder.add_p("The system boundary encompasses five distinct active and automated actors:")
    builder.add_bullet_item("Actor A1: System Administrator", "Authorized election official who creates election records, registers candidate nominations, imports voter rosters via CSV, and manages election closure.")
    builder.add_bullet_item("Actor A2: Registered Voter", "Authenticated participant who inspects candidate manifestos, casts an AES-256 encrypted ballot, and receives a cryptographic QR receipt.")
    builder.add_bullet_item("Actor A3: Independent Observer", "Third-party election monitor who reviews live vote tallies, inspects mined block headers, and monitors real-time AI fraud analytics.")
    builder.add_bullet_item("Actor A4: System Auditor", "Cryptographic verifier who audits the continuity of SHA-256 block hashes and validates Merkle root integrity.")
    builder.add_bullet_item("Actor A5: Automated AI Fraud Radar", "Automated background service analyzing vote arrival timestamps and IP clustering metrics to generate risk alerts.")
    builder.add_page_break()

    # Page 46: Figure 5.1 — System Use Case Diagram Specifications
    builder.add_section_heading("5.4 Use Case Model & Structural Boundaries")
    builder.add_p("The Use Case model defines the functional interactions across system boundaries between identified actors and internal use cases:")
    builder.add_diagram_box(
        "5.1", "System Use Case Diagram Specification", "Behavioral Use Case Model",
        [
            "Primary Actors: System Administrator, Registered Voter, Independent Observer, System Auditor.",
            "Core Administrative Use Cases: UC-01 User Authentication, UC-02 Create Election Instance, UC-03 Register Candidate, UC-04 Bulk CSV Voter Import.",
            "Core Voter Use Cases: UC-05 Browse Active Ballots, UC-06 Cast Encrypted Vote, UC-07 Download Cryptographic QR Receipt.",
            "Core Audit Use Cases: UC-08 Inspect Blockchain Ledger, UC-09 Execute Chain Cryptographic Audit, UC-10 Verify Individual Receipt Hash.",
            "Core Telemetry Use Cases: UC-11 Monitor Live Tally Distribution, UC-12 Review AI Fraud Radar Scoring.",
            "Archetypal Relationships: <<include>> Auth Check across all authenticated operations; <<extend>> AI Anomaly Flagging upon rapid-burst detection."
        ],
        image_filename="02_Use_Case.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.1 illustrates the complete use case hierarchy, highlighting the strict separation between administrative, voter, and auditing functions.")
    builder.add_page_break()

    # Page 47: Detailed Use Case Narrative: UC-01 & UC-02
    builder.add_section_heading("5.6 Detailed Use Case Specification: UC-01 User Authentication")
    builder.add_styled_table(
        ["Specification Attribute", "Use Case Narrative Details: UC-01 User Authentication"],
        [
            ["Use Case ID & Name", "UC-01: User Login & Session Establishment"],
            ["Primary Actor", "All System Users (Administrator, Voter, Observer)"],
            ["Preconditions", "User possesses registered account credentials in the SQLite database."],
            ["Trigger", "User enters email and password into login form and clicks 'Sign In'."],
            ["Main Success Scenario", "1. Client transmits credentials over TLS 1.3 to `/api/v1/auth/login`.\n2. Server retrieves user record and executes Bcrypt hash verification.\n3. Server signs and issues OAuth2 JWT Bearer token containing user ID and role.\n4. Client stores token in application state and redirects to role dashboard."],
            ["Alternative Flow", "Invalid credentials return HTTP 401 Unauthorized; system renders red error alert."],
            ["Postconditions", "Authenticated session established; token injected into subsequent Axios requests."]
        ],
        col_widths=[2.0, 4.0]
    )
    builder.add_section_heading("5.6 Detailed Use Case Specification: UC-02 Create Election Instance")
    builder.add_styled_table(
        ["Specification Attribute", "Use Case Narrative Details: UC-02 Create Election Instance"],
        [
            ["Use Case ID & Name", "UC-02: Election Instance Creation & Configuration"],
            ["Primary Actor", "System Administrator"],
            ["Preconditions", "Administrator authenticated with valid JWT token having role='admin'."],
            ["Main Success Scenario", "1. Admin enters Title, Description, and Schedule dates.\n2. Server creates election record in SQLite database with status='active'.\n3. System enables Candidate Nomination Studio for the new election."],
            ["Postconditions", "New election instance available for candidate registration and voter browsing."]
        ],
        col_widths=[2.0, 4.0]
    )
    builder.add_page_break()

    # Page 48: Detailed Use Case Narrative: UC-03 & UC-04
    builder.add_section_heading("5.6 Detailed Use Case Specification: UC-03 Candidate Registration")
    builder.add_styled_table(
        ["Specification Attribute", "Use Case Narrative Details: UC-03 Candidate Registration"],
        [
            ["Use Case ID & Name", "UC-03: Register Candidate Profile & Nomination"],
            ["Primary Actor", "System Administrator"],
            ["Preconditions", "Active election selected; administrator authenticated."],
            ["Main Success Scenario", "1. Admin inputs Candidate Name, Political Party, Manifesto summary, and Avatar URL.\n2. System validates input data against Pydantic schema.\n3. Record created in `candidates` table linked via foreign key to `election_id`.\n4. Candidate profile card rendered in Voter Dashboard."],
            ["Postconditions", "Candidate displayed on voter ballots with initial vote count of zero."]
        ],
        col_widths=[2.0, 4.0]
    )
    builder.add_section_heading("5.6 Detailed Use Case Specification: UC-04 Cast Encrypted Vote")
    builder.add_styled_table(
        ["Specification Attribute", "Use Case Narrative Details: UC-04 Cast Encrypted Vote"],
        [
            ["Use Case ID & Name", "UC-04: Cast Encrypted Ballot & Block Mining"],
            ["Primary Actor", "Registered Voter"],
            ["Preconditions", "Voter authenticated; election status='active'; voter has not voted in this election."],
            ["Main Success Scenario", "1. Voter clicks 'Vote for Candidate' on desired card.\n2. Vote payload encrypted using AES-256 GCM.\n3. Server calculates SHA-256 Merkle root and executes Proof-of-Work miner.\n4. Block signed via SECP256R1 ECDSA and added to chain.\n5. Cryptographic QR receipt modal displayed to voter."],
            ["Alternative Flow", "If voter has already voted, server returns HTTP 400 'Vote already cast in this election'."],
            ["Postconditions", "Vote permanently logged on blockchain; voter marked as voted; receipt generated."]
        ],
        col_widths=[2.0, 4.0]
    )
    builder.add_page_break()

    # Page 49: Detailed Use Case Narrative: UC-05 Receipt Audit & Chain Verification
    builder.add_section_heading("5.6 Detailed Use Case Specification: UC-05 Receipt Verification & Chain Audit")
    builder.add_styled_table(
        ["Specification Attribute", "Use Case Narrative Details: UC-05 Receipt Verification & Chain Audit"],
        [
            ["Use Case ID & Name", "UC-05: Cryptographic Receipt Verification & Full Ledger Audit"],
            ["Primary Actor", "Any User / Independent Election Observer / System Auditor"],
            ["Preconditions", "Valid SHA-256 transaction receipt hash string provided by voter."],
            ["Main Success Scenario: Receipt Lookup", "1. User enters 64-character receipt hash into search input on `/voter/receipts`.\n2. System traverses blockchain blocks to locate matching transaction.\n3. System validates transaction presence in block Merkle root.\n4. System returns Block Index, Timestamp, and 'Verified Authentic' confirmation badge."],
            ["Main Success Scenario: Full Chain Audit", "1. Auditor clicks 'Execute Full Chain Audit' on `/explorer`.\n2. Engine validates previous_hash continuity across all blocks from Genesis block.\n3. Engine verifies Proof-of-Work difficulty on all block headers.\n4. System returns chain validity status and cryptographic health score (100%)."],
            ["Postconditions", "Cryptographic proof of election integrity displayed without exposing voter ballot choice."]
        ],
        col_widths=[2.0, 4.0]
    )
    builder.add_p("Use-case specifications UC-01 through UC-05 encompass the full functional lifecycle of the application.")
    builder.add_page_break()

    # Page 50: Figure 5.2 — System Class Diagram Architecture
    builder.add_section_heading("5.8 Class Diagram Architecture & Entity Specifications")
    builder.add_p("The Class Diagram specifies the object-oriented structure of the system, defining domain models, service classes, attributes, methods, and relational cardinalities:")
    builder.add_diagram_box(
        "5.2", "System Class Diagram Architecture Specification", "Structural Class Model",
        [
            "Entity Classes: User (id, email, username, role, hashed_password), Election (id, title, status, dates), Candidate (id, party, manifesto), VoteReceipt (tx_hash, voter_hash, block_index).",
            "Cryptographic Class Block: index, timestamp, previous_hash, hash, nonce, merkle_root, signature; methods: calculate_hash(), mine_pow(difficulty=4), sign_block().",
            "Service Class BlockchainService: chain, pending_txs, difficulty; methods: create_genesis_block(), add_transaction(), mine_pending_blocks(), is_chain_valid().",
            "Service Class AIFraudService: vote_timestamps, ip_log; methods: log_vote(), check_burst_anomaly(threshold=500ms), calculate_risk_score() -> Float.",
            "Structural Cardinalities: User 1 ---- * VoteReceipt; Election 1 ---- * Candidate; Election 1 ---- * VoteReceipt; Block 1 ---- * Transaction."
        ],
        image_filename="03_Class_Diagram.png",
        img_width=4.4
    )
    builder.add_p("Figure 5.2 formalizes the data and behavioral encapsulation across all core software entities.")
    builder.add_page_break()

    # Page 51: Figure 5.3 — Sequence Diagram 1: Authentication Flow
    builder.add_section_heading("5.11 Sequence Diagram 1 — Authentication & JWT Issuance Flow")
    builder.add_diagram_box(
        "5.3", "Sequence Diagram — User Authentication & JWT Issuance", "Dynamic Behavioral Model",
        [
            "Participants: Client Browser (Voter/Admin), Auth API Router, SecurityService (Bcrypt), SQLite Database Engine, JWT Token Signer.",
            "Message 1: Client sends HTTP POST `/api/v1/auth/login` with email and password payload.",
            "Message 2: Auth Router queries SQLite Database: `SELECT * FROM users WHERE email = ?`.",
            "Message 3: Database returns User record including stored Bcrypt hashed_password.",
            "Message 4: Auth Router invokes `SecurityService.verify_password(input_password, hashed_password)`.",
            "Message 5: Bcrypt computation validates cryptographic equality.",
            "Message 6: Auth Router invokes `JWT.encode()` with payload `{sub: user.id, role: user.role, exp: 60m}` signed with HS256 secret key.",
            "Message 7: Server returns HTTP 200 OK containing JSON `{access_token: token, token_type: 'bearer', user: profile}`.",
            "Message 8: Client stores token in AuthContext and configures Axios request interceptors."
        ],
        image_filename="04_Login_Sequence.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.3 details the synchronous interaction flow governing user authentication and token issuance.")
    builder.add_page_break()

    # Page 52: Figure 5.4 — Sequence Diagram 2: Voter Registration Flow
    builder.add_section_heading("5.12 Sequence Diagram 2 — Voter Self-Registration Flow")
    builder.add_diagram_box(
        "5.4", "Sequence Diagram — Voter Self-Registration Flow", "Dynamic Behavioral Model",
        [
            "Participants: Voter Registration UI, Auth API Router, Pydantic Validator, SecurityService, SQLite Database.",
            "Message 1: Voter submits registration form containing email, username, and password.",
            "Message 2: Pydantic schema validates format correctness (email syntax, password complexity).",
            "Message 3: Auth Router queries SQLite: check duplicate `SELECT id FROM users WHERE email=? OR username=?`.",
            "Message 4: Database confirms zero conflicting records.",
            "Message 5: Auth Router invokes `SecurityService.hash_password(raw_password)` using Bcrypt cost factor 12.",
            "Message 6: Auth Router issues SQL: `INSERT INTO users (email, username, hashed_password, role) VALUES (?, ?, ?, 'voter')`.",
            "Message 7: Database commits new user record and returns assigned auto-incremented primary key `id`.",
            "Message 8: Server returns HTTP 201 Created with confirmation payload; Client UI renders success toast."
        ],
        image_filename="05_Registration_Sequence.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.4 outlines the registration sequence, highlighting duplicate identity checks and secure password hashing.")
    builder.add_page_break()

    # Page 53: Figure 5.5 — Sequence Diagram 3: Encrypted Vote Casting & Receipt Flow
    builder.add_section_heading("5.13 Sequence Diagram 3 — Encrypted Vote Casting & Receipt Flow")
    builder.add_diagram_box(
        "5.5", "Sequence Diagram — Encrypted Vote Casting & Receipt Generation", "Dynamic Behavioral Model",
        [
            "Participants: Voter Portal UI, Vote API Router, AES-256 Crypto Service, BlockchainService, SQLite DB, QRCode Modal.",
            "Message 1: Voter clicks 'Vote for Candidate'; UI prompts confirmation modal.",
            "Message 2: Voter confirms; UI computes voter hash and sends HTTP POST `/api/v1/votes/cast` with Bearer token.",
            "Message 3: Vote Router checks `VoteReceipt`: ensure voter has not previously voted in this `election_id`.",
            "Message 4: Vote Router invokes `AES256.encrypt(candidate_id, election_secret_key)` generating encrypted cipher payload.",
            "Message 5: Vote Router forwards transaction payload to `BlockchainService.enqueue_and_mine()`.",
            "Message 6: BlockchainService bundles transaction, calculates Merkle root, executes Proof-of-Work miner, and signs block.",
            "Message 7: Mined block metadata and SHA-256 receipt hash saved to SQLite `vote_receipts` table.",
            "Message 8: Server returns HTTP 200 OK with receipt JSON payload.",
            "Message 9: Client UI opens QRCodeModal displaying receipt hash, block index, and downloadable QR image."
        ],
        image_filename="06_Main_Workflow_Sequence.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.5 captures the core electoral transaction flow from ballot submission to cryptographic receipt rendering.")
    builder.add_page_break()

    # Page 54: Figure 5.6 — Sequence Diagram 4: Proof-of-Work & SECP256R1 Mining Flow
    builder.add_section_heading("5.14 Sequence Diagram 4 — Proof-of-Work Mining & SECP256R1 ECDSA Flow")
    builder.add_diagram_box(
        "5.6", "Sequence Diagram — Proof-of-Work Consensus Mining & ECDSA Sign", "Dynamic Behavioral Model",
        [
            "Participants: BlockchainService, MerkleCalculator, PoW Mining Loop, SECP256R1 Key Store, Ledger Storage.",
            "Message 1: `BlockchainService` receives batched transactions for block creation.",
            "Message 2: Invokes `MerkleCalculator.compute_root(transactions)`: recursive pairwise SHA-256 calculation.",
            "Message 3: MerkleCalculator returns 64-character hexadecimal Merkle root hash string.",
            "Message 4: Mining Loop initialized: `nonce = 0`, `target_prefix = '0000'`, `previous_hash = chain[-1].hash`.",
            "Message 5: While Loop computes `hash = SHA256(index + timestamp + previous_hash + merkle_root + nonce)`.",
            "Message 6: If `hash` does not start with '0000', increment `nonce` and repeat.",
            "Message 7: Hash collision found matching '0000'; loop terminates.",
            "Message 8: Invokes `SECP256R1.sign(block_hash, private_key)`: produces DER-encoded ECDSA signature.",
            "Message 9: Fully assembled block appended to `chain` array and broadcast to public ledger endpoints."
        ],
        image_filename="07_API_Sequence.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.6 visualizes the Proof-of-Work consensus algorithm and asymmetric digital signing process.")
    builder.add_page_break()

    # Page 55: Figure 5.7 — Sequence Diagram 5: Receipt Verification & Merkle Audit
    builder.add_section_heading("5.15 Sequence Diagram 5 — Receipt Verification & Merkle Audit Flow")
    builder.add_diagram_box(
        "5.7", "Sequence Diagram — Public Receipt Hash Verification & Chain Audit", "Dynamic Behavioral Model",
        [
            "Participants: Verification Portal UI, Public Blockchain Router, Blockchain Ledger Store, Merkle Verifier.",
            "Message 1: User pastes SHA-256 receipt hash into search input on `/voter/receipts` and clicks 'Verify'.",
            "Message 2: Client transmits HTTP GET `/api/v1/votes/verify-receipt/{receipt_hash}`.",
            "Message 3: Router iterates through all blocks in `Blockchain.chain` looking for matching transaction hash.",
            "Message 4: Matching transaction located in Block #N.",
            "Message 5: Router invokes `MerkleVerifier.validate_proof(tx_hash, block.merkle_root)`.",
            "Message 6: Verifier confirms transaction is mathematically bound to the block's Merkle root.",
            "Message 7: Router verifies block ECDSA signature against server's public key.",
            "Message 8: Server returns HTTP 200 OK containing JSON `{verified: true, block_index: N, timestamp: T, tx_hash: H}`.",
            "Message 9: Client UI renders green 'Verified On-Chain' audit certificate badge."
        ],
        image_filename="07_API_Sequence.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.7 illustrates the public verification workflow confirming that a voter's ballot is permanently recorded.")
    builder.add_page_break()

    # Page 56: Figure 5.8 — Activity Diagram 1: Voter Lifecycle Workflow
    builder.add_section_heading("5.16 Activity Diagram 1 — Voter Lifecycle Control Flow")
    builder.add_diagram_box(
        "5.8", "Activity Diagram — Voter Lifecycle & Voting Workflow", "Activity Control Flow",
        [
            "Initial Node: Voter opens application web URL.",
            "Decision 1: Is user authenticated? -> [No] Navigate to Login / Register form; -> [Yes] Load Dashboard.",
            "Activity 1: Fetch active elections list from `/api/v1/elections`.",
            "Activity 2: Voter selects target election and views nominated candidate cards.",
            "Decision 2: Has voter already cast a ballot in this election? -> [Yes] Disable Vote button, render 'Already Voted' badge; -> [No] Enable Candidate 'Vote' buttons.",
            "Activity 3: Voter selects desired candidate and confirms submission in dialog.",
            "Activity 4: System executes client-side AES-256 encryption and submits vote payload.",
            "Activity 5: Engine mines Proof-of-Work block, generates QR receipt, and updates ledger.",
            "Activity 6: System renders QRCodeModal; voter downloads PNG receipt and reviews TxHash.",
            "Final Node: Voter session concludes or navigates to receipt verification portal."
        ],
        image_filename="09_Main_Workflow_Activity.png",
        img_width=4.8
    )
    builder.add_p("Figure 5.8 models the complete decision logic and operational path experienced by a registered voter.")
    builder.add_page_break()

    # Page 57: Figure 5.9 — Activity Diagram 2: Admin Election Studio Workflow
    builder.add_section_heading("5.17 Activity Diagram 2 — Administrator Election Studio Workflow")
    builder.add_diagram_box(
        "5.9", "Activity Diagram — Administrator Election Studio Workflow", "Activity Control Flow",
        [
            "Initial Node: Administrator signs in with admin credentials.",
            "Activity 1: Administrator navigates to `/admin/elections` studio.",
            "Activity 2: Fills 'Create New Election' form (Title, Description, Scheduling).",
            "Activity 3: Submits form; server persists election with status='active'.",
            "Activity 4: Enters Candidate Nomination Studio; inputs candidate name, party, manifesto, avatar URL.",
            "Activity 5: Candidate profile saved and associated with election record.",
            "Activity 6 (Optional): Admin selects 'Import Voters CSV' and uploads student roster.",
            "Activity 7: Server parses CSV file and bulk-creates voter user accounts.",
            "Activity 8: Administrator monitors election progress via live Observer Dashboard.",
            "Activity 9: Election period concludes; Administrator toggles status to 'closed'.",
            "Final Node: Final blockchain tally locked; audit report published."
        ],
        image_filename="08_Login_Activity.png",
        img_width=4.8
    )
    builder.add_p("Figure 5.9 models the end-to-end management flow executed by election administrators.")
    builder.add_page_break()

    # Page 58: Figure 5.10 — Entity-Relationship (ER) Diagram Specifications
    builder.add_section_heading("5.19 Entity-Relationship (ER) Diagram Specifications")
    builder.add_p("The Entity-Relationship model defines relational database tables, primary/foreign keys, and cardinalities:")
    builder.add_diagram_box(
        "5.10", "Entity-Relationship (ER) Diagram Specification", "Relational Data Model",
        [
            "Table `users`: id (PK, Int, Auto), email (VarChar, Unique), username (VarChar, Unique), hashed_password (VarChar), role (VarChar), created_at (DateTime).",
            "Table `elections`: id (PK, Int, Auto), title (VarChar), description (Text), status (VarChar), start_time (DateTime), end_time (DateTime), created_by (Int, FK -> users.id).",
            "Table `candidates`: id (PK, Int, Auto), election_id (Int, FK -> elections.id), name (VarChar), party (VarChar), manifesto (Text), avatar_url (VarChar), vote_count (Int).",
            "Table `vote_receipts`: id (PK, Int, Auto), user_id (Int, FK -> users.id), election_id (Int, FK -> elections.id), candidate_id (Int, FK -> candidates.id), voter_hash (VarChar), encrypted_vote (Text), tx_hash (VarChar, Unique), block_index (Int), receipt_hash (VarChar, Unique), created_at (DateTime).",
            "Table `audit_logs`: id (PK, Int, Auto), user_id (Int), action (VarChar), details (Text), ip_address (VarChar), timestamp (DateTime).",
            "Cardinalities: users 1 ---- * elections (created_by); elections 1 ---- * candidates (election_id); elections 1 ---- * vote_receipts (election_id); users 1 ---- * vote_receipts (user_id)."
        ],
        image_filename="10_ER_Diagram.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.10 formalizes relational schemas and relational constraints enforced by SQLite and SQLAlchemy.")
    builder.add_page_break()

    # Page 59: Figure 5.11 — System Deployment Diagram Infrastructure
    builder.add_section_heading("5.21 Deployment Diagram Infrastructure Specifications")
    builder.add_p("The Deployment Diagram maps software artifacts to physical execution nodes and cloud environments:")
    builder.add_diagram_box(
        "5.11", "System Deployment Diagram Specification", "Physical Deployment Model",
        [
            "Execution Node 1 (Client Browser): React 19 Single Page App, LocalStorage Fallback, Web Crypto API via HTTPS (TLS 1.3).",
            "Execution Node 2 (Vercel Edge CDN): Global reverse proxy, static asset edge caching, and client-side route rewrite engine.",
            "Execution Node 3 (Render Cloud Server): Python 3.12, Uvicorn ASGI Worker, FastAPI REST Router, Blockchain & AI Services.",
            "Execution Node 4 (Database Storage Volume): SQLite 3 Database (`voting_system.db`) with Write-Ahead Logging (WAL) concurrency.",
            "Network Topologies: Browser connects via TLS 1.3 to Vercel CDN; Vercel CDN proxies API calls to Render Cloud; Render writes to SQLite."
        ],
        image_filename="11_Deployment.png",
        img_width=4.4
    )
    builder.add_p("Figure 5.11 details the multi-node infrastructure topology enabling high availability and decoupled scaling.")
    builder.add_page_break()

    # Page 60: Figure 5.12 — System Context Diagram
    builder.add_section_heading("5.22 System Context Diagram Specifications")
    builder.add_diagram_box(
        "5.12", "System Context Diagram Specification", "Top-Level Context Model",
        [
            "Central System Entity: Decentralized Blockchain Voting Platform.",
            "External Entity 1: Institutional Administrator (Transmits election parameters, candidate bios, voter CSV files; receives audit metrics).",
            "External Entity 2: Registered Voter (Transmits credentials and encrypted vote selections; receives cryptographic QR receipts).",
            "External Entity 3: Independent Election Observer (Transmits tally queries and block search filters; receives real-time vote distribution graphics).",
            "External Entity 4: External Security Auditor (Transmits Merkle root audit requests; receives cryptographic chain proof validation).",
            "External Entity 5: AI Telemetry Monitor (Continuously ingests request arrival rates; outputs fraud alert scores to Observer UI)."
        ],
        image_filename="01_System_Context.png",
        img_width=5.0
    )
    builder.add_p("Figure 5.12 defines the top-level operational context, identifying all external entities interacting across system boundaries.")
    builder.add_page_break()

    # Page 61: Figure 5.13 — Data Flow Diagram (DFD Level 0 — Context) & 5.24 Summary
    builder.add_section_heading("5.23 Data Flow Diagram (DFD Level 0 — Context)")
    builder.add_diagram_box(
        "5.13", "Data Flow Diagram (DFD Level 0 — Context Model)", "Data Flow Architecture",
        [
            "Process 0.0: Central Decentralized Blockchain Voting System Engine.",
            "External Entities: System Administrator, Registered Voter, Independent Observer / Auditor.",
            "Data Stores: D1 SQLite Relational Store, D2 Cryptographic Blockchain Ledger.",
            "Data Transformations: User credentials verified against D1; candidate rosters registered in D1; votes encrypted and mined into D2 blocks; QR receipts returned to voters; audit proofs served to observers."
        ],
        image_filename="14_DFD_Level_0.png",
        img_width=5.0
    )
    builder.add_section_heading("5.24 UML Diagram Cross-Verification & Chapter Summary")
    builder.add_p("The complete UML and DFD modeling suite established in Chapter 5 maintains rigorous consistency with the software implementation. Chapter 6 formalizes the multi-tier System Architecture Design.")

    builder.add_page_break()
