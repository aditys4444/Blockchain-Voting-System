# COMPLETE PROFESSIONAL UML DIAGRAM SET SPECIFICATION & INDEX
## Decentralized Blockchain Voting System with AI Fraud Radar
**Academic Session:** 2026 - 2027  
**Lead Engineer / Author:** Aditya Yadav (B.Sc Computer Science)  
**Standard:** UML 2.5 Specification Standard  

---

### SUMMARY OF GENERATED DIAGRAMS

| Diagram # | File Name | Diagram Title | Related Chapter | Core Requirements Grounding |
| :--- | :--- | :--- | :--- | :--- |
| **Figure 5.1** | `01_System_Context.png` | System Context Diagram | Chapter 1 & Chapter 5 | System Boundaries & External Actors |
| **Figure 5.2** | `02_Use_Case.png` | System Use Case Diagram | Chapter 3 & Chapter 5 | FR-01 to FR-25 Actor Functional Mapping |
| **Figure 5.3** | `03_Class_Diagram.png` | System Class Diagram Architecture | Chapter 5 & Chapter 7 | SQLAlchemy Models & Cryptographic Classes |
| **Figure 5.4** | `04_Login_Sequence.png` | Sequence Diagram: User Authentication | Chapter 3 & Chapter 5 | FR-01 (Bcrypt & OAuth2 JWT Bearer Flow) |
| **Figure 5.5** | `05_Registration_Sequence.png` | Sequence Diagram: Voter Self-Registration | Chapter 3 & Chapter 5 | FR-02 (Identity Creation & Duplicate Check) |
| **Figure 5.6** | `06_Main_Workflow_Sequence.png` | Sequence Diagram: Encrypted Vote Casting & Mining | Chapter 3 & Chapter 5 | FR-09, FR-10, FR-15, FR-16 (AES-256 & PoW) |
| **Figure 5.7** | `07_API_Sequence.png` | Sequence Diagram: API & AI Telemetry | Chapter 5 & Chapter 6 | FR-21 to FR-25 (Arrival Rate & WebSocket) |
| **Figure 5.8** | `08_Login_Activity.png` | Activity Diagram: User Login & Role Guard | Chapter 5 | FR-01, FR-03 (Decision Logic & Routing) |
| **Figure 5.9** | `09_Main_Workflow_Activity.png` | Activity Diagram: Voter Main Lifecycle | Chapter 5 | FR-09 to FR-12 (Voter Journey & QR Receipt) |
| **Figure 5.10** | `10_ER_Diagram.png` | Entity-Relationship (ER) Data Model | Chapter 5 & Chapter 7 | Relational Schema (`users`, `elections`, etc.) |
| **Figure 5.11** | `11_Deployment.png` | System Deployment Architecture Diagram | Chapter 6 | Vercel CDN Edge, Render Cloud & SQLite WAL |
| **Figure 5.12** | `12_Component.png` | UML Component Architecture Diagram | Chapter 6 & Chapter 7 | Multi-Tier Software Dependencies |
| **Figure 5.13** | `13_Module.png` | Package & Directory Module Diagram | Chapter 7 | Physical Folder & Import Hierarchy |
| **Figure 5.14** | `14_DFD_Level_0.png` | Data Flow Diagram (DFD Level 0 — Context) | Chapter 5 & Chapter 6 | External Entity Data Transformations |
| **Figure 5.15** | `15_DFD_Level_1.png` | Data Flow Diagram (DFD Level 1 — Decomposition)| Chapter 5 & Chapter 6 | Functional Sub-Process Data Flow |

---

## 1. DETAILED EXPLANATION OF EACH DIAGRAM

### Figure 5.1: System Context Diagram (`01_System_Context.png`)
- **Purpose:** Identifies the high-level boundary of the Decentralized Blockchain Voting System, demarcating external entities (System Administrator, Registered Voter, Independent Observer) from internal services and persistence stores.
- **Components:**
  - *External Users:* Administrator (provides election definitions and candidate nominations), Registered Voter (submits credentials and encrypted votes), Independent Observer (queries live standings and block explorer).
  - *Internal Core System:* React 19 Frontend SPA, FastAPI Asynchronous Web Engine, SECP256R1 ECDSA Signer, Proof-of-Work Miner, and AI Anomaly Radar.
  - *Data Stores:* SQLite Relational Database Engine (`voting_system.db`) and SHA-256 Blockchain Ledger.

### Figure 5.2: System Use Case Diagram (`02_Use_Case.png`)
- **Purpose:** Models the functional interactions between human and automated actors and the system's operational use cases.
- **Actors:**
  - `Administrator`: Interacts with `UC-01 Login`, `UC-02 Create Election`, `UC-03 Register Candidate`, `UC-04 Bulk CSV Import`.
  - `Registered Voter`: Interacts with `UC-01 Login`, `UC-05 Browse Active Ballots`, `UC-06 Cast Encrypted Ballot`, `UC-07 Download QR Receipt`.
  - `Independent Observer`: Interacts with `UC-10 Verify Receipt Hash`, `UC-11 Full Chain Audit`, `UC-12 AI Fraud Telemetry`.
  - `AI Fraud Engine`: Automated background actor that executes `<<extend>>` relationship on `UC-06` to score burst anomalies.
- **Include / Extend Relationships:**
  - `UC-06 Cast Encrypted Ballot` *<<includes>>* `UC-08 Mine PoW Block` and `UC-07 Download QR Receipt`.
  - `UC-08 Mine PoW Block` *<<includes>>* `UC-09 Sign Block with SECP256R1`.
  - `UC-06 Cast Encrypted Ballot` *<<extends>>* `UC-12 AI Fraud Telemetry Scoring` when transaction arrival interval < 500ms.

### Figure 5.3: System Class Diagram Architecture (`03_Class_Diagram.png`)
- **Purpose:** Formalizes the object-oriented structure, class attributes, method signatures, and relational associations based strictly on the project source code.
- **Classes:**
  - `User`: Handles identity credentials, password verification, and JWT generation.
  - `Election`: Manages election scheduling, status toggling, and candidate aggregation.
  - `Candidate`: Holds candidate nominations, manifestos, and real-time vote tallies.
  - `VoteReceipt`: Stores cryptographic transaction hashes, voter hashes, block indices, and public receipt hashes.
  - `Block`: Represents cryptographic blocks, calculating SHA-256 headers, mining Proof-of-Work nonces, and signing headers via SECP256R1.
  - `BlockchainService`: Maintains chain validity, pending transaction pools, and Merkle tree calculations.
- **Cardinality:**
  - `User` 1 ──── * `Election` (created_by)
  - `Election` 1 ──── * `Candidate` (election_id)
  - `User` 1 ──── * `VoteReceipt` (user_id)
  - `VoteReceipt` * ──── 1 `Block` (block_index)

### Figure 5.4: Sequence Diagram for User Login (`04_Login_Sequence.png`)
- **Purpose:** Details the synchronous step-by-step interaction between the client browser, FastAPI authentication router, Bcrypt security service, SQLite database, and JWT token generator.
- **Flow:**
  1. Client sends HTTP POST `/api/v1/auth/login`.
  2. Router queries database for matching email.
  3. Bcrypt validates password against stored hash.
  4. Server signs and issues OAuth2 JWT Bearer token containing user ID and role.
  5. Client stores token and redirects to role dashboard.

### Figure 5.5: Sequence Diagram for Voter Self-Registration (`05_Registration_Sequence.png`)
- **Purpose:** Models the registration sequence, verifying input formatting, enforcing duplicate identity checks, and salting passwords.
- **Flow:**
  1. Voter submits registration form.
  2. System checks for duplicate email or username.
  3. SecurityService generates Bcrypt hash (work factor 12).
  4. Database inserts new user record with `role='voter'`.
  5. Server returns HTTP 201 Created and initiates automated session login.

### Figure 5.6: Sequence Diagram for Encrypted Voting & Mining (`06_Main_Workflow_Sequence.png`)
- **Purpose:** Visualizes the end-to-end voting process from ballot submission to Proof-of-Work block mining and QR receipt display.
- **Flow:**
  1. Voter clicks 'Vote for Candidate'.
  2. System validates voter has not previously voted in this election.
  3. Vote payload encrypted with AES-256 GCM.
  4. Miner batches transaction and calculates SHA-256 Merkle root.
  5. Mining loop finds nonce satisfying difficulty 4 zero-prefixes (`0000`).
  6. Mined block header signed via SECP256R1 private key.
  7. Receipt metadata committed to database.
  8. Client UI renders QRCodeModal with receipt hash.

### Figure 5.7: Sequence Diagram for API Interaction & AI Fraud Telemetry (`07_API_Sequence.png`)
- **Purpose:** Details how incoming API requests feed the real-time AI Fraud Radar engine.
- **Flow:**
  1. Client transmits request with Bearer token.
  2. Gateway logs arrival timestamp and client IP.
  3. Velocity engine calculates inter-arrival time $\Delta t$.
  4. Bursts <500ms trigger anomaly risk score recalculation.
  5. WebSockets broadcaster pushes updated tallies and risk scores to Observer portal in real time.

### Figure 5.8: Activity Diagram for User Login (`08_Login_Activity.png`)
- **Purpose:** Illustrates the control flow, decision branches, error paths, and role-based redirects during authentication.
- **Decisions:**
  - *Valid Hash?* [No] -> Display HTTP 401 error toast and permit retry; [Yes] -> Issue JWT.
  - *User Role?* [admin] -> Redirect `/admin/elections`; [voter] -> Redirect `/voter`; [observer] -> Redirect `/observer`.

### Figure 5.9: Activity Diagram for Voter Main Workflow (`09_Main_Workflow_Activity.png`)
- **Purpose:** Models the voter lifecycle from ballot selection to QR receipt acquisition.
- **Control Flow:** Authenticate -> Fetch active elections -> Decision: *Already Voted?* [Yes] -> Navigate to `/receipts`; [No] -> Select candidate -> Encrypt AES-256 -> Mine PoW block -> Display QRCodeModal -> Exit.

### Figure 5.10: Entity-Relationship (ER) Data Model (`10_ER_Diagram.png`)
- **Purpose:** Specifies relational tables, primary keys, foreign keys, and cardinalities in the SQLite database.
- **Entities:** `USERS` (1:N to `ELECTIONS`), `ELECTIONS` (1:N to `CANDIDATES`), `ELECTIONS` (1:N to `VOTE_RECEIPTS`), `USERS` (1:N to `VOTE_RECEIPTS`), `USERS` (1:N to `AUDIT_LOGS`).

### Figure 5.11: System Deployment Diagram (`11_Deployment.png`)
- **Purpose:** Details the hardware execution nodes, cloud runtime environments, and network communication protocols.
- **Nodes:** Client Browser Node (React 19 SPA + LocalStorage fallback), Vercel Global Edge CDN (TLS 1.3 reverse proxy), Render Cloud Container (Uvicorn ASGI + Python 3.12), Persistent Storage Volume (SQLite 3 WAL database).

### Figure 5.12: UML Component Diagram (`12_Component.png`)
- **Purpose:** Shows modular software components and their interface dependencies.
- **Components:** UI Presentation Component, REST API Component, Security & Auth Component, Blockchain Ledger Engine, AI Fraud Radar Service, Database Storage Layer.

### Figure 5.13: Package & Directory Module Diagram (`13_Module.png`)
- **Purpose:** Maps the physical directory organization of the software repository, detailing package imports and inter-module dependencies across `frontend/src/`, `backend/app/`, and `backend/blockchain/`.

### Figure 5.14: Data Flow Diagram (DFD Level 0 — Context) (`14_DFD_Level_0.png`)
- **Purpose:** Visualizes data inputs, transformations, and outputs flowing between external actors, Process 0.0, and data stores (D1 SQLite, D2 Blockchain Ledger).

### Figure 5.15: Data Flow Diagram (DFD Level 1 — Decomposition) (`15_DFD_Level_1.png`)
- **Purpose:** Decomposes Process 0.0 into five functional sub-processes: `1.0 User Authentication`, `2.0 Election Management`, `3.0 Ballot Encryption`, `4.0 Block Mining & Consensus`, and `5.0 AI Fraud Telemetry`.
