# Software Requirements Specification (SRS) & Architecture Report
## Blockchain Voting System — Major Project

**Document Version:** 1.0  
**Prepared By:** TYBSc Computer Science / AI-ML Project Team  
**Institution:** Thakur Ramnarayan College of Arts & Commerce (TRCAC)  
**Date:** August 2026  
**Status:** Final Draft Project Report  

---

## Table of Contents
1. Introduction
   - 1.1 Purpose
   - 1.2 Scope
   - 1.3 Definitions & Acronyms
   - 1.4 References
   - 1.5 Overview
2. Overall Description
   - 2.1 Product Perspective
   - 2.2 Product Functions (High-Level)
   - 2.3 User Classes & Characteristics
   - 2.4 Operating Environment
   - 2.5 Design & Implementation Constraints
   - 2.6 Assumptions & Dependencies
3. User Roles & Characteristics
   - 3.1 Admin
   - 3.2 Voter
   - 3.3 Observer
4. Functional Requirements
   - 4.1 Authentication & Authorization Module
   - 4.2 Admin Dashboard & Election Management Module
   - 4.3 Voter Dashboard & Voting Module
   - 4.4 Custom Blockchain Engine Module
   - 4.5 Observer Transparency & Analytics Module
   - 4.6 AI Fraud Radar & Anomaly Detection Module
5. Non-Functional Requirements
   - 5.1 Performance
   - 5.2 Security
   - 5.3 Reliability
   - 5.4 Usability
   - 5.5 Scalability
   - 5.6 Maintainability
6. System Constraints
7. External Interface Requirements
   - 7.1 User Interfaces
   - 7.2 Hardware Interfaces
   - 7.3 Software Interfaces
   - 7.4 Communication Interfaces
8. Data Requirements & Schema
   - 8.1 Data Entities & Schema Description
   - 8.2 Data Retention
   - 8.3 Data Integrity
9. Complete Set of UML Diagrams Specifications
   - 9.1 Use Case Diagrams
   - 9.2 Class Diagrams
   - 9.3 Sequence Diagrams (Login Flow, Voting & Mining Flow)
   - 9.4 Activity Diagram (Auto-Attendance / AI Fraud Velocity Marking)
   - 9.5 Component Diagram (Three-Tier Architecture)
   - 9.6 Entity-Relationship (ER) Diagram
10. Architecture Design Document (ADD)
   - 10.1 Architectural Goals
   - 10.2 System Context Diagram
   - 10.3 Three-Tier Model Specifications
   - 10.4 Frontend & Backend Architecture
   - 10.5 Custom Blockchain Architecture
   - 10.6 Key Design Decisions & Tradeoffs Matrix

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document details the complete functional, non-functional, and architectural requirements for the **Blockchain Voting System**. It acts as the primary technical specification for developers, project evaluators, security auditors, and stakeholders.

### 1.2 Scope
The **Blockchain Voting System** is a modern, full-stack, decentralized web platform designed to conduct tamper-evident e-elections. It features a custom Python cryptographic engine (SHA-256, Proof-of-Work, Merkle Trees, ECDSA SECP256R1), role-based access control, AES-256 GCM vote payload encryption, real-time WebSockets analytics, an AI Fraud Radar, and downloadable QR code receipts.

| User Role | Module Scope & Privileges |
| :--- | :--- |
| **Admin** | Full election creation, candidate management, CSV bulk voter import, system metrics, audit logs, blockchain health. |
| **Voter** | Active election viewing, 1-click encrypted voting, downloadable QR receipts, vote hash verification on ledger. |
| **Observer** | Public transparency desk, live Recharts vote tallies, public block explorer, AI fraud radar. |

### 1.3 Definitions & Acronyms

| Term | Definition |
| :--- | :--- |
| **SRS** | Software Requirements Specification |
| **ADD** | Architecture Design Document |
| **PoW** | Proof-of-Work mining consensus algorithm |
| **ECDSA** | Elliptic Curve Digital Signature Algorithm (SECP256R1) |
| **AES-256 GCM** | Advanced Encryption Standard with Galois/Counter Mode |
| **JWT** | JSON Web Token for stateless session authorization |
| **RBAC** | Role-Based Access Control |
| **Merkle Tree** | Cryptographic binary hash tree aggregating block transactions |

---

## 2. Overall Description

### 2.1 Product Perspective
The system is a standalone web application replacing traditional paper ballot casting. It connects a React 19 + Vite frontend to a FastAPI Python backend, backed by SQLite / PostgreSQL database and an in-memory custom SHA-256 Blockchain ledger engine.

### 2.2 High-Level Product Functions
1. **User Authentication**: Role logins (Admin, Voter, Observer) with bcrypt password hashing.
2. **Election Studio**: Admin creates, edits, activates, and closes elections.
3. **Candidate Studio**: Candidate registration with party affiliation, manifesto, and avatar URL.
4. **Bulk Enrollment**: CSV file upload for bulk voter account generation.
5. **1-Click Encrypted Voting**: AES-256 GCM payload encryption + ECDSA digital signature.
6. **Proof-of-Work Block Mining**: Packages queued transactions into blocks meeting SHA-256 difficulty targets.
7. **QR Receipts**: Downloadable receipts containing receipt hash, block index, and transaction hash.
8. **Blockchain Explorer**: Public block browser, transaction search, and 1-click ledger tamper auditor.
9. **AI Fraud Radar**: Analyzes vote velocity bursts (<2s), duplicate IP concentration, and flags threat scores (0-100%).

---

## 3. User Roles & Characteristics

### 3.1 Admin
- **Technical Level**: Moderate to High.
- **Typical Tasks**: Create elections, manage candidates, upload voter CSVs, view audit logs, check blockchain health.

### 3.2 Voter
- **Technical Level**: Basic to Moderate.
- **Typical Tasks**: Select candidate in active election, submit encrypted vote, generate QR code receipt, verify receipt hash.

### 3.3 Observer
- **Technical Level**: Basic to High.
- **Typical Tasks**: View live vote standings, inspect block ledger, verify chain integrity, view AI fraud alerts.

---

## 4. Functional Requirements

### 4.1 Authentication & Authorization Module
- **FR-AUTH-01: User Login**: Authenticates email/username and password using bcrypt. Returns JWT access token (24h expiry) and refresh token.
- **FR-AUTH-02: Role Protection**: Protected endpoints enforce role permissions (`admin`, `voter`, `observer`). Returns HTTP 401/403 for unauthorized requests.

### 4.2 Election & Candidate Management
- **FR-ADMIN-01: Create Election**: Admin creates elections with title, description, start/end dates.
- **FR-ADMIN-02: Candidate Management**: Admin registers candidates with party name, manifesto, and avatar URL.
- **FR-ADMIN-03: Bulk Voter Import**: Admin uploads CSV containing `email`, `username`, and `password` to generate voter accounts.

### 4.3 Voting & Blockchain Engine
- **FR-VOTE-01: Cast Vote**: Single vote per voter per election. Votes are encrypted with AES-256 GCM and signed with voter ECDSA keypair.
- **FR-VOTE-02: Anti-Double Voting**: Enforces unique database constraints. Duplicate attempts are blocked and logged in audit trails.
- **FR-CHAIN-01: Block Mining**: Transactions packaged into blocks. Miner computes SHA-256 hash meeting difficulty target (2 zero prefix).
- **FR-CHAIN-02: Merkle Tree Generation**: Computes binary hash root for all transactions within a block.
- **FR-CHAIN-03: Ledger Explorer & Audit**: Search block by index/hash or transaction by hash. 1-click full chain tamper check.

---

## 5. Non-Functional Requirements

### 5.1 Performance
- API response time < 500ms for standard data endpoints.
- Block mining time < 2s under PoW difficulty 2.

### 5.2 Security
- AES-256 GCM vote payload encryption.
- ECDSA SECP256R1 digital signatures for transaction authenticity.
- bcrypt password hashing with salt rounds.
- Strict CORS whitelist and JWT Bearer authorization headers.

### 5.3 Usability
- Responsive glassmorphism interface built with React 19, Tailwind CSS, and Framer Motion.
- Dark/Light mode toggle for visual comfort.

---

## 8. Data Requirements & Database Schema

```text
+-------------------+       +--------------------+       +-------------------+
|      users        |       |     elections      |       |    candidates     |
+-------------------+       +--------------------+       +-------------------+
| id (PK)           |<----->| id (PK)            |<----->| id (PK)           |
| email (Unique)    |       | title              |       | election_id (FK)  |
| username (Unique) |       | description        |       | name              |
| hashed_password   |       | status             |       | party             |
| role              |       | start_time         |       | manifesto         |
| created_at        |       | end_time           |       | vote_count        |
+-------------------+       +--------------------+       +-------------------+
          |                           |
          v                           v
+------------------------------------------------+
|                     votes                      |
+------------------------------------------------+
| id (PK)                                        |
| user_id (FK)                                   |
| election_id (FK)                               |
| candidate_id (FK)                              |
| voter_hash (Indexed)                           |
| encrypted_vote                                 |
| tx_hash (Unique)                               |
| block_index                                    |
| receipt_hash (Unique)                          |
+------------------------------------------------+
```

---

## 10. Key Design Decisions & Tradeoffs Matrix

| # | Decision Area | Chosen Solution | Rationale | Tradeoff |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Ledger Engine | Custom Python Blockchain | Zero gas fees, instant mining, full control over block structure & PoW difficulty. | Not decentralized across multi-organization nodes (MVP single server). |
| **2** | Vote Confidentiality | AES-256 GCM Encryption | Prevents plaintext vote selections from being visible in public block explorer. | Server holds symmetric key for tallying. |
| **3** | Voter Authenticity | ECDSA SECP256R1 Signatures | Asymmetric digital key pairs guarantee transactions cannot be forged. | Single-use voter keypairs must be generated per vote. |
| **4** | Real-Time Updates | FastAPI WebSockets | Instant push broadcasts of vote counts and block additions without polling. | Requires active WebSocket connection handling. |
| **5** | Threat Monitoring | AI Heuristic Velocity Engine | Detects vote bursts (<2s), duplicate IP clusters, and double-voting attempts. | Rule-based anomaly detection requires tuning thresholds. |
