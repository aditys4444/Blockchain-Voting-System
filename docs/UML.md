# UML Diagrams — Complete Set
## Blockchain Voting System — Cryptographic E-Voting Module

**Document Version:** 1.0  
**Prepared By:** Student Project Team (TYBSc CS / AI-ML)  
**Institution:** Thakur Ramnarayan College of Arts & Commerce (TRCAC)  
**Date:** July 2026  

---

## Table of Contents
1. Use Case Diagram
2. Class Diagram
3. Sequence Diagram — Login Flow
4. Sequence Diagram — Encrypted Vote & Block Mining Flow
5. Sequence Diagram — Receipt Verification Flow
6. Activity Diagram — AI Fraud Detection & Velocity Marking
7. Component Diagram
8. ER Diagram (Database Schema)

---

## 1. Use Case Diagram

### 1.1 Admin Use Cases
- Login / Logout
- Create Student/Voter Account
- Create Election & Add Candidates
- Bulk Enroll Voters via CSV
- View System Dashboard Stats & Blockchain Health
- View & Download Immutable Audit Logs

### 1.2 Voter Use Cases
- Login / Logout
- View Active Elections & Candidate Profiles
- Cast Encrypted Vote (1-Click AES-256 + ECDSA Signature)
- Download QR Code Receipt
- Verify Receipt Hash on Blockchain Ledger

### 1.3 Observer Use Cases
- View Live Recharts Standings & Vote Percentages
- Inspect Mined Block Ledger & Merkle Roots
- Search Block by Index/Hash or Transaction Hash
- Trigger 1-Click Cryptographic Chain Audit
- View AI Fraud Radar & Velocity Alerts

---

## 2. Class Diagram

### 2.1 User & Auth Classes
```text
+------------------------------------------+
|                  User                    |
+------------------------------------------+
| +id: Integer                             |
| +email: String                           |
| +username: String                        |
| +hashed_password: String                 |
| +role: String (admin/voter/observer)     |
| +created_at: DateTime                    |
+------------------------------------------+
| +login()                                 |
+------------------------------------------+
```

### 2.2 Content & Block Classes
```text
+------------------------------------------+       +------------------------------------------+
|                 Block                    |       |                Blockchain                |
+------------------------------------------+       +------------------------------------------+
| +index: Integer                          |       | +chain: List[Block]                      |
| +timestamp: Float                        |       | +pending_transactions: List[Dict]        |
| +previous_hash: String                   |------>| +difficulty: Integer                     |
| +hash: String                            |       | +system_public_key: String               |
| +nonce: Integer                          |       +------------------------------------------+
| +merkle_root: String                     |       | +mine_pending_transactions()             |
| +signature: String                       |       | +is_chain_valid()                        |
+------------------------------------------+       | +search_block()                          |
| +calculate_hash()                        |       +------------------------------------------+
+------------------------------------------+
```

---

## 3. Sequence Diagram — Login Flow

```text
Student/Admin           Frontend (React)             FastAPI Server              Database (SQLite/PostgreSQL)
    |                          |                           |                                   |
    |---- Enter credentials -->|                           |                                   |
    |                          |-- POST /api/v1/auth/login->|                                   |
    |                          |                           |-- Search User by email/username -->|
    |                          |                           |<-- User record returned ----------|
    |                          |                           |-- Verify bcrypt password --------|
    |                          |                           |-- Generate JWT Access Token -----|
    |                          |<-- 200 {token, profile} --|                                   |
    |                          |-- Save to localStorage --|                                   |
    |<-- Redirect Dashboard ---|                           |                                   |
```

---

## 4. Sequence Diagram — Encrypted Vote & Block Mining Flow

```text
Voter                  React Frontend              FastAPI Server            Blockchain Engine            Database
  |                           |                          |                           |                       |
  |-- Click Select Candidate->|                          |                           |                       |
  |                           |-- Encrypt AES-256 GCM -->|                           |                       |
  |                           |-- Sign ECDSA SECP256R1 ->|                           |                       |
  |                           |-- POST /api/v1/votes/cast|                           |                       |
  |                           |                          |-- Check single-vote rule->|                       |
  |                           |                          |-- Add transaction -------->|                       |
  |                           |                          |                           |-- Mine PoW Block ---->|
  |                           |                          |                           |-- Calculate Merkle -->|
  |                           |                          |<-- Block mined #index ----|                       |
  |                           |                          |-- Save Vote & Block ----------------------------->|
  |                           |                          |-- Broadcast WebSockets ->|                       |
  |                           |<-- 200 {receipt_hash} ---|                           |                       |
  |<-- Show QR Code Receipt --|                          |                           |                       |
```
