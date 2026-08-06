import time
from typing import List, Dict, Any, Optional, Tuple
from .block import Block
from .cryptography import CryptoEngine

class Blockchain:
    """
    Custom Python Blockchain Engine for secure, immutable voting.
    Supports Genesis Block creation, Proof-of-Work mining, Merkle integrity checks, 
    and full chain validity auditing.
    """
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.difficulty = difficulty
        
        # System mining keypair for signing block headers
        self.system_private_key, self.system_public_key = CryptoEngine.generate_key_pair()
        
        # Initialize Genesis Block
        self.create_genesis_block()

    def create_genesis_block(self):
        """Generate the initial Genesis block (Index 0)."""
        genesis_tx = [{
            "tx_hash": CryptoEngine.sha256("GENESIS_INIT_VOTE_SYSTEM"),
            "election_id": 0,
            "voter_hash": "SYSTEM_00000000000000000000000000000000",
            "encrypted_vote": "GENESIS_BLOCK",
            "timestamp": time.time(),
            "signature": "SYSTEM_GENESIS_SIGNATURE"
        }]
        genesis_block = Block(
            index=0,
            transactions=genesis_tx,
            previous_hash="0" * 64,
            nonce=0
        )
        # Mine genesis block
        genesis_block.hash = self.proof_of_work(genesis_block)
        genesis_block.signature = CryptoEngine.sign_data(self.system_private_key, genesis_block.hash)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, transaction: Dict[str, Any]) -> str:
        """
        Validate and queue a vote transaction.
        Returns the computed transaction hash.
        """
        if not transaction.get("tx_hash"):
            transaction["tx_hash"] = CryptoEngine.hash_dict(transaction)
        
        self.pending_transactions.append(transaction)
        return transaction["tx_hash"]

    def proof_of_work(self, block: Block) -> str:
        """
        Proof-of-Work algorithm: Find nonce such that block hash begins 
        with target number of zeros (defined by difficulty).
        """
        block.nonce = 0
        computed_hash = block.calculate_hash()
        target_prefix = '0' * self.difficulty

        while not computed_hash.startswith(target_prefix):
            block.nonce += 1
            computed_hash = block.calculate_hash()
            
        return computed_hash

    def mine_pending_transactions(self) -> Optional[Block]:
        """
        Package pending transactions into a new Block, execute PoW, 
        sign the block, and append to the chain.
        """
        if not self.pending_transactions:
            return None

        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=list(self.pending_transactions),
            previous_hash=latest_block.hash
        )

        # Mine block (Proof-of-Work)
        new_block.hash = self.proof_of_work(new_block)
        
        # Sign mined block with system key
        new_block.signature = CryptoEngine.sign_data(self.system_private_key, new_block.hash)

        # Add to chain & clear pending queue
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self) -> Tuple[bool, str]:
        """
        Audit entire blockchain for tamper evidence:
        1. Check previous block hash links
        2. Re-verify Proof-of-Work hashes
        3. Re-verify Merkle Root of transactions in each block
        4. Re-verify Block signature
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 1. Link integrity check
            if current_block.previous_hash != previous_block.hash:
                return False, f"Broken chain link at Block #{current_block.index}. Previous hash mismatch."

            # 2. Hash computation check
            if current_block.hash != current_block.calculate_hash():
                return False, f"Tampered block hash at Block #{current_block.index}."

            # 3. Proof-of-Work check
            if not current_block.hash.startswith('0' * self.difficulty):
                return False, f"Invalid Proof-of-Work at Block #{current_block.index}."

            # 4. Merkle Root check
            computed_merkle = Block(
                index=current_block.index,
                transactions=current_block.transactions,
                previous_hash=current_block.previous_hash
            ).merkle_root
            if current_block.merkle_root != computed_merkle:
                return False, f"Merkle Root discrepancy at Block #{current_block.index}."

            # 5. Block signature check
            is_sig_valid = CryptoEngine.verify_signature(
                self.system_public_key,
                current_block.signature,
                current_block.hash
            )
            if not is_sig_valid:
                return False, f"Invalid block digital signature at Block #{current_block.index}."

        return True, "Blockchain integrity verified. 0 anomalies detected."

    def search_block(self, search_term: str) -> Optional[Block]:
        """Search block by Index or Block Hash."""
        for block in self.chain:
            if str(block.index) == str(search_term) or block.hash == search_term:
                return block
        return None

    def search_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Search transaction by Transaction Hash."""
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("tx_hash") == tx_hash:
                    return {
                        "transaction": tx,
                        "block_index": block.index,
                        "block_hash": block.hash,
                        "timestamp": block.timestamp
                    }
        return None

    def to_list(self) -> List[Dict[str, Any]]:
        """Export full chain to list of block dicts."""
        return [b.to_dict() for b in self.chain]
