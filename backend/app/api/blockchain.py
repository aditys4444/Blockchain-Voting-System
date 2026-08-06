from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..services.blockchain_service import blockchain_service
from ..schemas.schemas import BlockSchema, ChainStatusSchema

router = APIRouter(prefix="/blockchain", tags=["Blockchain Explorer"])

@router.get("/blocks", response_model=List[BlockSchema])
def get_all_blocks():
    return blockchain_service.blockchain.to_list()

@router.get("/blocks/{search_term}")
def get_block_by_search(search_term: str):
    block = blockchain_service.blockchain.search_block(search_term)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block.to_dict()

@router.get("/transactions/{tx_hash}")
def get_transaction_by_hash(tx_hash: str):
    tx_res = blockchain_service.blockchain.search_transaction(tx_hash)
    if not tx_res:
        raise HTTPException(status_code=404, detail="Transaction hash not found in blockchain ledger")
    return tx_res

@router.get("/status", response_model=ChainStatusSchema)
def get_blockchain_status():
    is_valid, msg = blockchain_service.blockchain.is_chain_valid()
    return {
        "is_valid": is_valid,
        "total_blocks": len(blockchain_service.blockchain.chain),
        "difficulty": blockchain_service.blockchain.difficulty,
        "pending_transactions_count": len(blockchain_service.blockchain.pending_transactions),
        "message": msg
    }

@router.get("/verify-chain")
def run_full_chain_audit():
    is_valid, msg = blockchain_service.blockchain.is_chain_valid()
    return {
        "chain_valid": is_valid,
        "audit_timestamp": float(blockchain_service.blockchain.get_latest_block().timestamp),
        "total_blocks_audited": len(blockchain_service.blockchain.chain),
        "audit_details": msg,
        "crypto_algorithms": ["SHA-256", "ECDSA SECP256R1", "Merkle Tree Root", "Proof-of-Work"]
    }
