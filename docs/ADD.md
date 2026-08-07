# Architecture Design Document (ADD)
## Blockchain Voting System — Cryptographic E-Voting Module

**Version:** 1.0 | **Date:** July 2026 | **Scope:** Full-Stack Decoupled Architecture  

---

## 1. Introduction & Goals

This document describes the structural design of the **Blockchain Voting System** — how it is organized, why key architectural decisions were made, and how all parts connect.

### Architectural Goals

| Goal | Description |
| :--- | :--- |
| **Separation of Concerns** | UI never touches database directly — frontend React SPA and backend FastAPI REST API are fully decoupled. |
| **Role-Based Security** | Every protected route enforces strict Admin / Voter / Observer role checks via JWT claims. |
| **Stateless Auth** | JWT-based authentication allows multiple backend instances without shared session state. |
| **Tamper Immutability** | Votes are recorded in SHA-256 blocks with Merkle roots and Proof-of-Work headers. |
| **Vote Confidentiality** | Candidate selections encrypted with AES-256 GCM prior to block inclusion. |

---

## 2. System Context

### 2.1 Actors and External Systems

| Actor / System | Type | Role |
| :--- | :--- | :--- |
| **Admin** | User | Creates accounts, manages elections, candidate profiles, bulk CSV voter enrollment. |
| **Voter** | User | Casts encrypted vote, views active elections, generates QR receipt, verifies hash. |
| **Observer** | User | Monitors live Recharts standings, inspects block explorer, checks AI alerts. |
| **SQLite / PostgreSQL** | External Service | Relational NoSQL/SQL database for application state persistence. |
| **Custom Blockchain** | Core Engine | SHA-256 PoW miner, Merkle tree generator, ECDSA signature verifier. |
| **Vercel / Docker** | External Service | Hosts static React SPA CDN and containerized ASGI backend service. |

---

## 3. Overall Architecture — Three-Tier Model

### 3.1 Architecture Layers

```text
[ Tier 1 — Presentation ]
Browser  <--->  React 19 + Vite + Tailwind CSS (SPA)
                        |
                 JSON / REST / WebSockets
                        v
[ Tier 2 — Application ]
FastAPI Python 3.12 Server (JWT Auth, AI Fraud Radar, WebSockets)
                        |
                        v
[ Tier 3 — Data & Ledger ]
Custom SHA-256 Blockchain Engine <---> SQLite / PostgreSQL Database
```

---

## 4. Frontend Architecture

### 4.1 Technology Stack

| Technology | Version | Role |
| :--- | :--- | :--- |
| **React** | 19.0 | UI Component Library |
| **Vite** | 5.x | Build tool & HMR dev server |
| **React Router DOM** | 6.x | Client-side declarative routing |
| **Tailwind CSS** | 3.4 | Utility-first styling & Dark Mode |
| **Framer Motion** | 11.x | Smooth page transitions and micro-interactions |
| **Recharts** | 2.x | Live vote distribution charts |
| **Axios** | 1.x | HTTP client with JWT auth interceptors |

---

## 5. Backend Architecture

### 5.1 Technology Stack

| Technology | Version | Role |
| :--- | :--- | :--- |
| **Node.js / Python** | 3.12+ | Server runtime environment |
| **FastAPI** | 0.111+ | Web framework |
| **SQLAlchemy** | 2.0+ | Database ORM mapping |
| **PyJWT** | 2.8+ | JWT auth tokens |
| **bcrypt** | 4.1+ | Password hashing |
| **Cryptography** | 42.0+ | AES-256 GCM & ECDSA SECP256R1 algorithms |

---

## 6. Key Design Decisions Matrix

| # | Decision | Choice | Rationale | Tradeoff |
| :-: | :--- | :--- | :--- | :--- |
| **1** | User storage | Unified `users` table | Simplified auth query logic across roles. | Requires explicit role authorization checks on routes. |
| **2** | Vote Secrecy | AES-256 GCM Encryption | Prevents plaintext vote choices from showing in block explorer. | Server key required for decryption during tallying. |
| **3** | Voter Auth | ECDSA SECP256R1 Key Pairs | Asymmetric digital key pairs guarantee transactions cannot be forged. | Single-use keypairs generated per vote. |
| **4** | Real-Time Updates | FastAPI WebSockets | Instant push broadcasts of vote counts and block additions. | Active WebSocket connection handling. |
| **5** | Threat Monitoring | Heuristic Velocity Engine | Detects vote bursts (<2s), duplicate IP clusters, and double-voting. | Thresholds require tuning for scale. |
