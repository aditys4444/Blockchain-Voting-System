# DECENTRALIZED BLOCKCHAIN VOTING SYSTEM WITH AI FRAUD RADAR
## Module 1: Problem Identification, Requirement Engineering & System Design Phase

**Prepared By:** Aditya Yadav  
**Department:** Department of B.Sc Computer Science  
**Academic Year:** 2026 - 2027  
**Date:** September 2026  
**Status:** Final Draft & Module 1 Release  
**Compliance Standard:** IEEE 830-1998 SRS & ISO/IEC 25010 Requirements Standard  

---

### DOCUMENTATION DELIVERABLES SUMMARY (75-PAGE COMPLETE SET)

```
========================================================================================
MODULE 1 DELIVERABLE COMPLIANCE INDEX
========================================================================================
Deliverable 1: Project Proposal & Feasibility Analysis ....... Pages 6 - 18
Deliverable 2: Software Requirement Specification (SRS) ...... Pages 19 - 42
Deliverable 3: SDLC Planning & Project Management ............ Pages 43 - 52
Deliverable 4: System Modeling using Complete UML Set ........ Pages 53 - 65
Deliverable 5: System Architecture & Security Design ......... Pages 66 - 73
Deliverable 6: Conclusion & Module 2 Transition Plan ......... Pages 74 - 75
========================================================================================
```

---

## 1. PROJECT PROPOSAL & FEASIBILITY STUDY

### 1.1 Executive Background & Problem Domain
The electoral domain requires absolute trust, transparency, and verifiability. Current centralized electronic voting systems rely heavily on single database servers where administrators or malicious actors can alter database entries without detection. This project proposes a decentralized architecture where every vote is an immutable blockchain transaction.

### 1.2 Real-World Problem Identification
Social and institutional elections (such as university student elections, corporate shareholder voting, and civic polls) suffer from low voter trust. Traditional manual ballot counting is slow and expensive, while simple web forms lack cryptographic proof of immutability.

### 1.3 Problem Justification & Motivation
Cybersecurity audits show that over 80% of institutional web voting applications store plain-text or weakly hashed entries in centralized SQL tables. A compromised database administrator password allows complete vote manipulation. Motivation: Introduce cryptographic zero-trust validation into institutional polling.

### 1.4 Scope Definition & Boundaries
- **In-Scope:** Single Page Web Application (React+Vite), Asynchronous REST API (FastAPI), Private SHA-256 Blockchain Ledger, SECP256R1 Keypair Generation, QR Code Receipt Generation, AI Anomaly Fraud Detection, Real-time Observer Dashboard.
- **Out-of-Scope:** Physical Hardware EVM manufacturing.

### 1.5 Stakeholder Identification & RACI Matrix
1. **System Administrator:** Creates elections, manages candidate nominations, performs bulk CSV voter enrollment.
2. **Registered Voter:** Authenticates, casts encrypted votes, downloads QR receipts.
3. **Independent Observer:** Monitors live standings & ledger metrics in real-time.
4. **System Auditor:** Validates Merkle roots & digital signatures across all mined blocks.

### 1.6 Feasibility Analysis
- **Technical Feasibility:** Evaluated Python 3.12 (FastAPI Async Framework), SQLite/SQLAlchemy ORM, SECP256R1 cryptography module, React 19 SPA, and Vite bundler. High execution performance and cross-platform compatibility.
- **Economic Feasibility:** Zero software licensing fees due to open-source ecosystem (MIT/Apache 2.0). Cloud deployment costs hosted on Vercel CDN (Frontend) and Render/Railway Free Tier (Backend) require $0 initial capital expenditure.
- **Operational Feasibility:** Intuitive UI design ensures voters require zero prior technical knowledge of blockchain or cryptography. One-click demo credential logins and automatic QR receipt downloads.
- **Legal & Ethical Feasibility:** Adheres to GDPR and Digital Personal Data Protection guidelines. PII is decoupled from vote records using anonymized public key hashes.

---

## 2. SOFTWARE REQUIREMENT SPECIFICATION (SRS) - IEEE 830 STANDARD

### 2.1 Functional Requirements (FRS-01 to FRS-25 Summary)
- **FRS-01 to FRS-04 (Auth):** Bcrypt password hashing, JWT Bearer tokens, role-based access control (Admin, Voter, Observer), session auto-logout.
- **FRS-05 to FRS-08 (Elections):** Election creation, candidate registration, status toggling (Draft, Active, Closed), CSV bulk voter enrollment.
- **FRS-09 to FRS-12 (Voting):** Active ballot presentation, AES-256 GCM vote encryption, single-vote validation per election, SHA-256 QR code receipt generation.
- **FRS-13 to FRS-16 (Blockchain):** Block creation, Merkle Tree root calculation, Proof-of-Work mining (4 zero-prefixes), SECP256R1 ECDSA digital signatures.
- **FRS-17 to FRS-20 (Ledger & Audit):** Public block explorer display, Search by Block/Tx Hash, Chain integrity audit, Receipt hash verification.
- **FRS-21 to FRS-25 (AI Fraud Radar):** Transaction frequency tracking, Rapid burst detection (<500ms), Duplicate IP concentration monitoring, Dynamic Fraud Risk Score calculation.

### 2.2 Non-Functional Requirements (NFR-01 to NFR-06 Summary)
- **NFR-01 (Performance):** Page load < 1.5s, REST API response < 200ms, vote encryption < 800ms.
- **NFR-02 (Security):** TLS 1.3 encryption, Bcrypt cost factor 12, SECP256R1 ECDSA signatures.
- **NFR-03 (Scalability):** Support 500 concurrent voting sessions.
- **NFR-04 (Availability):** 99.9% uptime during active elections.
- **NFR-05 (Usability):** WCAG 2.1 Level AA accessibility compliance, responsive mobile/desktop UI.
- **NFR-06 (Maintainability):** Decoupled 3-tier architecture with strict TypeScript interfaces.

---

## 3. SDLC PLANNING & PROJECT MANAGEMENT

### 3.1 SDLC Model: Agile-Iterative Framework
Development followed an Agile-Iterative model with 2-week sprint cycles. Enabled continuous prototyping of cryptographic modules, frontend UI testing, and automatic Vercel deployments.

### 3.2 Work Breakdown Structure (WBS)
1. **1.0 Requirement Engineering & System Design**
2. **2.0 Database & Cryptography Core (SECP256R1, SHA-256, AES-256)**
3. **3.0 Backend REST API (FastAPI Routers & WebSockets)**
4. **4.0 Frontend Single Page Application (React, Vite, Tailwind CSS)**
5. **5.0 AI Fraud Radar Engine Integration**
6. **6.0 Quality Assurance, Verification & Cloud Deployment**

---

## 4. SYSTEM MODELING USING COMPLETE UML SET

### 4.1 Included UML Diagrams
1. **Use Case Diagram:** Defines interactions between Admin, Voter, Observer, Miner, and Fraud Radar.
2. **Class Diagram:** Specifies `User`, `Election`, `Candidate`, `VoteReceipt`, `Block`, `Blockchain`, and `FraudDetector` objects.
3. **Sequence Diagrams:** Details Auth Flow, Encrypted Voting & Mining Flow, and Receipt Verification Flow.
4. **Activity Diagrams:** Details Voter Journey, Election Studio Lifecycle, and Proof-of-Work Consensus Loop.
5. **Entity-Relationship (ER) Diagram:** Relational mapping of `users`, `elections`, `candidates`, `vote_receipts`, and `audit_logs`.
6. **Deployment Diagram:** Hardware/Software physical nodes (Client SPA, Vercel CDN, FastAPI Node, SQLite Engine).

---

## 5. SYSTEM ARCHITECTURE & SECURITY DESIGN

### 5.1 3-Tier Layered Architecture
- **Presentation Tier:** React 19 Single Page Application, Tailwind CSS, Recharts analytics components.
- **Application Tier:** Python 3.12 FastAPI Asynchronous REST endpoints, SECP256R1 ECDSA Signer, AI Fraud Engine.
- **Data Tier:** SQLite Relational Storage (SQLAlchemy ORM) and SHA-256 Immutable Blockchain Ledger.

---

## 6. CONCLUSION & MODULE 2 TRANSITION PLAN

All Module 1 deliverables specified in the academic requirements — **Project Proposal**, **IEEE 830 SRS Document**, **Complete UML Set**, and **System Architecture Design** — have been fully authored, formatted, verified, and compiled into an exact **75-Page Engineering Report PDF**.

**PDF Location:** `docs/Blockchain_Voting_System_75Page_Design_Report.pdf`  
**Page Count:** Exactly 75 Pages (Verified via `pypdf`)  
