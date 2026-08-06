from typing import Dict, Any
from .cryptography import CryptoEngine

class VoterWallet:
    """
    Voter cryptographic wallet helper.
    Generates single-use ECDSA keypairs for voter anonymity and vote receipt verification.
    """
    @staticmethod
    def create_voter_credentials(voter_id: int, election_id: int) -> Dict[str, Any]:
        priv, pub = CryptoEngine.generate_key_pair()
        voter_hash = CryptoEngine.sha256(f"VOTER_{voter_id}_ELECTION_{election_id}")
        return {
            "voter_hash": voter_hash,
            "private_key": priv,
            "public_key": pub
        }

    @staticmethod
    def generate_receipt(
        tx_hash: str,
        block_index: int,
        voter_hash: str,
        election_id: int
    ) -> Dict[str, Any]:
        """Generate structured metadata for downloadable QR receipt."""
        receipt_raw = f"{tx_hash}:{block_index}:{voter_hash}:{election_id}"
        receipt_hash = CryptoEngine.sha256(receipt_raw)
        return {
            "transaction_hash": tx_hash,
            "block_index": block_index,
            "voter_hash": voter_hash,
            "election_id": election_id,
            "receipt_hash": receipt_hash,
            "verification_url": f"/verify-receipt?hash={receipt_hash}"
        }
