import time
import json
from typing import List, Dict, Any
from .cryptography import CryptoEngine

class MerkleTree:
    """
    Computes cryptographic Merkle Root Hash for a set of transactions.
    Ensures transaction integrity within a block.
    """
    @staticmethod
    def compute_root(transactions: List[Dict[str, Any]]) -> str:
        if not transactions:
            return CryptoEngine.sha256("EMPTY_TREE")
        
        # Extract transaction hashes
        tx_hashes = [
            tx.get("tx_hash") or CryptoEngine.hash_dict(tx) 
            for tx in transactions
        ]

        # Duplicate last hash if odd count
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])
            
            new_level = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i + 1]
                new_level.append(CryptoEngine.sha256(combined))
            tx_hashes = new_level
            
        return tx_hashes[0]


class Block:
    """
    Represents an immutable Block in the Blockchain.
    """
    def __init__(
        self,
        index: int,
        transactions: List[Dict[str, Any]],
        previous_hash: str,
        nonce: int = 0,
        timestamp: float = None,
        merkle_root: str = None,
        block_hash: str = None,
        signature: str = ""
    ):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root or MerkleTree.compute_root(transactions)
        self.hash = block_hash or self.calculate_hash()
        self.signature = signature

    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block contents."""
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }
        return CryptoEngine.hash_dict(block_content)

    def to_dict(self) -> Dict[str, Any]:
        """Convert block instance to dictionary format."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root,
            "hash": self.hash,
            "signature": self.signature
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """Reconstruct Block object from dictionary data."""
        return cls(
            index=data["index"],
            transactions=data["transactions"],
            previous_hash=data["previous_hash"],
            nonce=data["nonce"],
            timestamp=data["timestamp"],
            merkle_root=data["merkle_root"],
            block_hash=data["hash"],
            signature=data.get("signature", "")
        )
