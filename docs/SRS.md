# Software Requirements Specification (SRS)
## Blockchain Voting System (BVS)
### Cryptographic E-Voting & Decentralized Ledger Module

**Document Version:** 1.0  
**Prepared By:** Aditya Yadav  
**Department:** B.Sc. Computer Science  
**Institution:** Thakur Ramnarayan College of Arts & Commerce (TRCAC)  
**Academic Year:** 2026–2027  
**Date:** August 2026  
**Status:** Final Draft  

---

## Table of Contents & Executive Summary

### Executive Summary
The **Blockchain Voting System (BVS)** is an enterprise-grade, decentralized electronic voting platform designed to ensure 100% tamper-evident election integrity, voter confidentiality, and real-time public auditability. By leveraging SHA-256 Proof-of-Work block mining, binary Merkle Tree digests, AES-256 GCM ballot payload encryption, and ECDSA digital signatures, BVS provides a mathematically verifiable voting process suitable for academic institutions, corporate governance, and civic bodies.

### Table of Contents
1. **Introduction** — Project purpose, scope, intended audience, definitions, and IEEE references.
2. **Overall Description** — System context, operational modules, and end-to-end election workflow.
3. **User Roles & Characteristics** — Admin, Voter, and Observer personas, access levels, and responsibilities.
4. **Functional Requirements** — Core features across auth, elections, candidates, voting, blockchain, and AI.
5. **Non-Functional Requirements** — Security, performance, reliability, usability, scalability, and maintainability.
6. **System Constraints** — Technical, environmental, and operational constraints and assumptions.
7. **External Interface Requirements** — UI philosophy, full page inventory mapping, and 12-page detailed design.
8. **Data Requirements** — Complete 3NF database schema, key indexes, and entity relationships.
9. **Entity Relationship Summary** — Detailed entity connectivity and multiplicity mapping.
10. **Compliance & Sign-Off** — IEEE 830 compliance matrix and formal approval sign-off block.

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document defines the functional and non-functional requirements for the Blockchain Voting System (BVS). The system is designed to digitise, secure, and streamline the complete election cycle — encompassing voter registration, candidate nomination, 1-click encrypted voting, Proof-of-Work block mining, and verifiable cryptographic receipts.

### 1.2 Project Scope
The Blockchain Voting System is a web-based multi-role application that centralises end-to-end election operations. The system covers:
- User profile and voter eligibility management
- Election scheduling and lifecycle state management (Draft / Active / Closed)
- Candidate registration and manifesto management
- 1-Click encrypted ballot casting with AES-256 GCM encryption
- Asymmetric digital signature signing via ECDSA SECP256R1
- Proof-of-Work block mining and binary Merkle Tree computation
- Downloadable QR code receipts and hash verification desk
- AI Fraud Radar tracking vote velocity bursts and duplicate IP clusters
- Real-time election standings and audit trail logging

### 1.3 Intended Audience & Stakeholders
- **Software Development Team:** Design, develop, and integrate system modules per specifications.
- **Project Manager:** Track deliverables, milestones, and scope boundaries.
- **QA / Testing Team:** Derive test cases, security benchmarks, and acceptance criteria.
- **Institutional Administration:** Validate that requirements reflect institutional election needs.
- **Election Officer / Auditor:** Primary end-user; manages day-to-day elections and reviews audit logs.
- **System Administrator:** Understand roles, access levels, server deployment, and security policies.

### 1.4 Definitions and Abbreviations
- **BVS:** Blockchain Voting System
- **PoW:** Proof-of-Work consensus algorithm for computational block mining
- **ECDSA:** Elliptic Curve Digital Signature Algorithm (SECP256R1 curve)
- **AES-256 GCM:** Advanced Encryption Standard with Galois/Counter Mode authenticated encryption
- **SHA-256:** Secure Hash Algorithm 256-bit cryptographic digest function
- **Merkle Tree:** Cryptographic binary hash tree aggregating all transactions within a block
- **SRS:** Software Requirements Specification
- **RBAC:** Role-Based Access Control
- **JWT:** JSON Web Token — stateless cryptographic bearer token for authentication
- **FK / PK:** Foreign Key / Primary Key — database relational identifiers
- **TRCAC:** Thakur Ramnarayan College of Arts & Commerce

### 1.5 References
- IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications
- ISO/IEC 25010:2011: Systems and Software Quality Requirements and Evaluation
- OWASP Security Guidelines for Web Applications (v4.0)
- NIST Special Publication 800-38D (GCM Block Cipher Mode)
- SEC 2: Recommended Elliptic Curve Domain Parameters (SECP256R1)
- Tailwind CSS and React 19 Component Library Documentation
- FastAPI Asynchronous Web Framework Documentation (v0.111+)

---

## 2. Overall Description

### 2.1 System Context & High-Level Architecture
The BVS is a centralised, browser-based platform accessible via standard browsers. The system operates on a decoupled Three-Tier Architecture:
1. **Presentation Tier:** React 19 + Vite Single Page Application (SPA) styled with Tailwind CSS
2. **Application Tier:** FastAPI (Python 3.12) REST API & WebSockets Event Manager
3. **Data & Ledger Tier:** Custom Python SHA-256 Blockchain Engine & SQLite / PostgreSQL Relational Database

### 2.2 System Modules Breakdown
1. **User Management:** Registration, authentication, bcrypt password hashing, role assignment.
2. **Election Management:** Election creation, scheduling, status lifecycle (Draft/Active/Closed).
3. **Candidate Management:** Candidate registration, manifestos, party affiliations, avatar URLs.
4. **Voting & Encryption:** AES-256 GCM encrypted ballots signed with ECDSA keypairs.
5. **Blockchain Engine:** Transaction packaging, SHA-256 PoW block mining, binary Merkle roots.
6. **Receipt & Verification:** Cryptographic QR receipts and public receipt hash verification.
7. **AI Fraud Radar:** Velocity burst detection (<2s), duplicate IP clusters, threat index (0-100%).
8. **Observer & Analytics:** Real-time vote tallies, turnout percentages, interactive Recharts charts.
9. **Reports & Audit:** Immutable audit logs, system metrics, CSV data export.
10. **WebSockets Broadcast:** Real-time push event manager broadcasting live updates.

---

## 3. User Roles & Characteristics

### 3.1 User Roles Summary
- **Administrator:** Full system access; manages users, roles, elections, candidates, bulk CSV enrollment, and platform configuration.
- **Voter:** Views active elections, reviews candidates, casts encrypted votes, downloads QR receipts, and verifies hashes.
- **Observer / Auditor:** Monitors live standings, inspects block explorer, audits blockchain integrity, and views AI fraud alerts.

---

## 4. Functional Requirements

### 4.1 Authentication & Authorization Module
- `FR-AUTH-01`: Secure login using email/username and password credentials with bcrypt hashing.
- `FR-AUTH-02`: Admin user creation specifying username, email, password, and role.
- `FR-AUTH-03`: Logout clearing client-side JWT token storage.
- `FR-AUTH-04`: Bearer token verification on protected endpoints checking role permissions.
- `FR-AUTH-05`: Password update with current password verification.

### 4.2 User Management Module
- `FR-USER-01`: Searchable, paginated table of all registered users.
- `FR-USER-02`: Role assignment (Admin, Voter, Observer) upon account creation.
- `FR-USER-03`: Account activation and deactivation toggle.
- `FR-USER-04`: Audit trail logging for user creation, role reassignment, and status changes.

### 4.3 Election Lifecycle Management Module
- `FR-ELEC-01`: Election creation with title, description, start date, and end date.
- `FR-ELEC-02`: State transition between Draft, Active, and Closed.
- `FR-ELEC-03`: Active elections automatically published to voter ballots.

### 4.4 Candidate Nomination Studio Module
- `FR-CAND-01`: Register candidate nominations with full name, party, manifesto, and avatar URL.
- `FR-CAND-02`: Manifesto popups on voter ballot interface.

### 4.5 1-Click Encrypted Voting Module
- `FR-VOTE-01`: 1-Click vote casting confirmation.
- `FR-VOTE-02`: AES-256 GCM authenticated payload encryption.
- `FR-VOTE-03`: ECDSA SECP256R1 digital transaction signing.
- `FR-VOTE-04`: Single vote enforcement per voter per election.

### 4.6 Receipt Generation & Hash Verification Module
- `FR-RCPT-01`: Printable QR code receipt containing receipt hash, block index, and tx hash.
- `FR-RCPT-02`: Public verification desk checking receipt hash against mined blockchain ledger.

### 4.7 Custom Blockchain Engine & Mining Module
- `FR-CHAIN-01`: SHA-256 Proof-of-Work block mining with difficulty target = 2.
- `FR-CHAIN-02`: Binary Merkle Root computation.
- `FR-CHAIN-03`: Interactive Blockchain Explorer and 1-click tamper detection audit.

### 4.8 AI Fraud Radar & Anomaly Detection Module
- `FR-AI-01`: Real-time submission timestamp and IP address monitoring.
- `FR-AI-02`: Velocity burst detection (<2s) and IP cluster detection.
- `FR-AI-03`: Composite Threat Index (0-100%) and risk level assignment (Low/Medium/High/Critical).

---

## 5. Non-Functional Requirements

### 5.1 Security Requirements
- bcrypt password hashing with salt rounds = 10.
- Enforced HTTPS (TLS 1.2+).
- AES-256 GCM vote payload encryption and ECDSA SECP256R1 signatures.
- Stateless 24-hour JWT Bearer tokens.

### 5.2 Performance Requirements
- API response time < 500ms.
- Block mining time < 2s under difficulty target = 2.
- Supports 500+ concurrent active voters.
- WebSockets updates pushed within 1 second.

---

## 6. System Constraints & Assumptions
1. Frontend built with React 19 + Tailwind CSS.
2. Backend built with Python 3.12 + FastAPI.
3. Proof-of-Work difficulty target set to 2 leading zeros.
4. Single vote policy enforced by compound uniqueness `(user_id, election_id)`.

---

## 7. External Interface Requirements

### 7.1 Page Inventory & Role Mapping
1. **Login / Register** — Public
2. **Dashboard** — All Roles
3. **User Management** — Admin
4. **Election Management** — Admin
5. **Candidate Studio** — Admin
6. **Bulk Voter Import** — Admin
7. **Voter Dashboard** — Voter
8. **QR Vote Receipt** — Voter
9. **Receipt Verification** — All Roles
10. **Blockchain Explorer** — All Roles
11. **Observer Dashboard** — Observer, Admin
12. **AI Fraud Radar** — Admin, Observer

---

## 8. Data Requirements (Database Schema)

### 8.1 Data Entities
- **USER:** `user_id (PK)`, `name`, `email (UNIQUE)`, `password`, `role_id (FK)`, `is_active`
- **ELECTION:** `election_id (PK)`, `title`, `description`, `status`, `start_time`, `end_time`, `created_by (FK)`
- **CANDIDATE:** `candidate_id (PK)`, `election_id (FK)`, `name`, `party`, `manifesto`, `avatar_url`, `vote_count`
- **VOTE:** `vote_id (PK)`, `user_id (FK)`, `election_id (FK)`, `candidate_id (FK)`, `voter_hash`, `encrypted_vote`, `tx_hash (UNIQUE)`, `block_index`, `receipt_hash (UNIQUE)`
- **BLOCK:** `block_id (PK)`, `block_index (UNIQUE)`, `timestamp`, `previous_hash`, `hash (UNIQUE)`, `nonce`, `merkle_root`, `signature`
- **TRANSACTION:** `tx_id (PK)`, `tx_hash (UNIQUE)`, `block_index (FK)`, `election_id (FK)`, `voter_hash`, `encrypted_vote`, `signature`
- **AI_ANOMALY:** `anomaly_id (PK)`, `election_id (FK)`, `anomaly_type`, `ip_address`, `risk_score`, `timestamp`
- **AUDIT_LOG:** `log_id (PK)`, `user_id (FK)`, `user_email`, `action`, `details`, `ip_address`, `timestamp`

---

## 9. Entity Relationship Summary
- `ROLE (1) -> USER (many)`
- `USER (1) -> VOTE (many)` *(enforces unique compound constraint `(user_id, election_id)`)*
- `ELECTION (1) -> CANDIDATE (many)`
- `ELECTION (1) -> VOTE (many)`
- `BLOCK (1) -> TRANSACTION (many)`
- `ELECTION (1) -> AI_ANOMALY (many)`
- `USER (1) -> AUDIT_LOG (many)`

---

## 10. Compliance Verification & Sign-Off
Complies with **IEEE Std 830-1998** standards.
- **Prepared By:** Aditya Yadav (B.Sc. Computer Science) — Approved & Verified
- **Department Reviewer:** TRCAC Department of Computer Science — Approved August 2026
- **Project Evaluator:** Academic Project Review Committee — Accepted for System Build
