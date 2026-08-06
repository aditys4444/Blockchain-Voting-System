# System Architecture & Cryptographic Workflow

## Overview
The **Blockchain Voting System** guarantees end-to-end vote confidentiality, immutability, and transparency by decoupling voter identity from block transaction content using asymmetric cryptography (ECDSA SECP256R1) and AES-256 GCM vote payload encryption.

```mermaid
graph TD
    A[Voter UI React 19] -->|1. Submit Candidate Selection| B[FastAPI Endpoint /votes/cast]
    B -->|2. Generate Voter Wallet| C[ECDSA Keypair & Voter Hash]
    B -->|3. Encrypt Vote Payload| D[AES-256 GCM Cipher]
    B -->|4. Create Transaction & Sign| E[Digital Signature SECP256R1]
    E -->|5. Queue Transaction| F[Custom Python Blockchain Engine]
    F -->|6. Calculate Merkle Tree Root| G[Merkle Root Hash]
    F -->|7. Proof-of-Work Mining| H[Find Nonce for Zero-Prefix Hash]
    H -->|8. Append Mined Block| I[Immutable Chain Ledger]
    I -->|9. Sync DB & Broadcast| J[SQLAlchemy DB + WebSockets]
    J -->|10. Generate QR Receipt| K[Voter QR Receipt Modal]
```

## Cryptographic Guarantees
1. **Vote Anonymity**: Votes are stored linked to `voter_hash` derived via SHA-256 salted hashes, never exposing plaintext voter names in blocks.
2. **AES-256 GCM Encryption**: Candidate selections are encrypted before block inclusion.
3. **ECDSA SECP256R1 Digital Signatures**: Every vote transaction is signed using a unique voter private key to verify authenticity.
4. **Merkle Tree Integrity**: Every mined block aggregates transactions into a binary hash tree. Any alteration invalidates the Merkle Root.
5. **Proof-of-Work Ledger**: Miners compute target zero-prefix block hashes, preventing retroactive tampering of previous blocks.
