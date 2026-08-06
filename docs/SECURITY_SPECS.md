# Security Specifications & AI Fraud Radar

## Security Mechanisms
1. **Password Hashing**: Passwords stored using bcrypt with salted rounds.
2. **JWT Sessions & Refresh Tokens**: Role-Based Access Control (`admin`, `voter`, `observer`) with expiration limits.
3. **AES-256 GCM Encryption**: Vote payload encrypted symmetrically before queuing into transaction pool.
4. **ECDSA SECP256R1 Digital Signatures**: Every vote transaction is signed via asymmetric private keys.
5. **Anti-Double Voting**: Single vote constraint per election per user, backed by database constraints & audit logging.

## AI Fraud Radar Module
- **Velocity Burst Detection**: Scans timestamps of submitted votes. Flags rapid bursts occurring < 2.0 seconds apart.
- **IP Concentration Risk**: Identifies anomalous IP addresses originating > 5 votes.
- **Double-Vote Audit Logs**: Captures blocked duplicate voting attempts and assigns weighted risk penalties.
- **Fraud Risk Score Index**: Computes unified threat score from 0.0% to 100.0% with dynamic risk level categorization (Low, Medium, High, Critical).
