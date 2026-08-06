import time
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
try:
    from blockchain.chain import Blockchain
    from blockchain.cryptography import CryptoEngine
except ImportError:
    from ...blockchain.chain import Blockchain
    from ...blockchain.cryptography import CryptoEngine
from ..models.models import BlockModel, TransactionModel
from ..core.config import settings

class BlockchainService:
    """
    Singleton Blockchain service manager.
    Synchronizes in-memory Python Blockchain engine with database persistence.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BlockchainService, cls).__new__(cls)
            cls._instance.blockchain = Blockchain(difficulty=settings.BLOCKCHAIN_DIFFICULTY)
        return cls._instance

    def initialize_from_db(self, db: Session):
        """Load existing blocks from DB if available."""
        db_blocks = db.query(BlockModel).order_by(BlockModel.index.asc()).all()
        if db_blocks:
            # Reconstruct chain from DB
            self.blockchain.chain = []
            for db_b in db_blocks:
                # Fetch transactions for block
                db_txs = db.query(TransactionModel).filter(TransactionModel.block_index == db_b.index).all()
                tx_list = [{
                    "tx_hash": tx.tx_hash,
                    "election_id": tx.election_id,
                    "voter_hash": tx.voter_hash,
                    "encrypted_vote": tx.encrypted_vote,
                    "timestamp": tx.timestamp,
                    "signature": tx.signature
                } for tx in db_txs]

                block = BlockModel(
                    index=db_b.index,
                    timestamp=db_b.timestamp,
                    previous_hash=db_b.previous_hash,
                    hash=db_b.hash,
                    nonce=db_b.nonce,
                    merkle_root=db_b.merkle_root,
                    signature=db_b.signature
                )
                try:
                    from blockchain.block import Block
                except ImportError:
                    from ...blockchain.block import Block
                reconstructed = Block(
                    index=db_b.index,
                    transactions=tx_list,
                    previous_hash=db_b.previous_hash,
                    nonce=db_b.nonce,
                    timestamp=db_b.timestamp,
                    merkle_root=db_b.merkle_root,
                    block_hash=db_b.hash,
                    signature=db_b.signature or ""
                )
                self.blockchain.chain.append(reconstructed)
        else:
            # Persist Genesis Block to DB
            genesis = self.blockchain.chain[0]
            db_b = BlockModel(
                index=genesis.index,
                timestamp=genesis.timestamp,
                previous_hash=genesis.previous_hash,
                hash=genesis.hash,
                nonce=genesis.nonce,
                merkle_root=genesis.merkle_root,
                signature=genesis.signature
            )
            db.add(db_b)
            for tx in genesis.transactions:
                db_tx = TransactionModel(
                    tx_hash=tx["tx_hash"],
                    block_index=genesis.index,
                    election_id=tx["election_id"],
                    voter_hash=tx["voter_hash"],
                    encrypted_vote=tx["encrypted_vote"],
                    timestamp=tx["timestamp"],
                    signature=tx["signature"]
                )
                db.add(db_tx)
            db.commit()

    def process_vote_transaction(
        self,
        db: Session,
        election_id: int,
        voter_hash: str,
        encrypted_vote: str,
        signature: str
    ) -> Tuple[str, int]:
        """
        Record transaction, mine block immediately (MVP mode), and persist to database.
        Returns (tx_hash, block_index).
        """
        tx = {
            "tx_hash": CryptoEngine.sha256(f"{election_id}:{voter_hash}:{encrypted_vote}:{time.time()}"),
            "election_id": election_id,
            "voter_hash": voter_hash,
            "encrypted_vote": encrypted_vote,
            "timestamp": time.time(),
            "signature": signature
        }

        # Queue transaction
        tx_hash = self.blockchain.add_transaction(tx)
        
        # Mine block immediately for instant vote confirmation
        new_block = self.blockchain.mine_pending_transactions()
        
        # Persist block to DB
        db_b = BlockModel(
            index=new_block.index,
            timestamp=new_block.timestamp,
            previous_hash=new_block.previous_hash,
            hash=new_block.hash,
            nonce=new_block.nonce,
            merkle_root=new_block.merkle_root,
            signature=new_block.signature
        )
        db.add(db_b)

        db_tx = TransactionModel(
            tx_hash=tx["tx_hash"],
            block_index=new_block.index,
            election_id=election_id,
            voter_hash=voter_hash,
            encrypted_vote=encrypted_vote,
            timestamp=tx["timestamp"],
            signature=signature
        )
        db.add(db_tx)
        db.commit()

        return tx_hash, new_block.index

blockchain_service = BlockchainService()
