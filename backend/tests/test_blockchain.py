import pytest
import time
from backend.blockchain.cryptography import CryptoEngine
from backend.blockchain.block import Block, MerkleTree
from backend.blockchain.chain import Blockchain

def test_crypto_engine_hashing():
    hash1 = CryptoEngine.sha256("test_data")
    hash2 = CryptoEngine.sha256("test_data")
    assert hash1 == hash2
    assert len(hash1) == 64

def test_ecdsa_signatures():
    priv, pub = CryptoEngine.generate_key_pair()
    data = "vote_payload_123"
    sig = CryptoEngine.sign_data(priv, data)
    assert len(sig) > 0
    assert CryptoEngine.verify_signature(pub, sig, data) is True
    assert CryptoEngine.verify_signature(pub, sig, "tampered_data") is False

def test_aes_vote_encryption():
    key = b"12345678901234567890123456789012"
    vote = "candidate_5"
    encrypted = CryptoEngine.encrypt_vote(vote, key)
    decrypted = CryptoEngine.decrypt_vote(encrypted, key)
    assert decrypted == vote

def test_merkle_tree():
    txs = [
        {"tx_hash": "hash1"},
        {"tx_hash": "hash2"},
        {"tx_hash": "hash3"}
    ]
    root = MerkleTree.compute_root(txs)
    assert len(root) == 64

def test_blockchain_mining_and_validation():
    bc = Blockchain(difficulty=1)
    assert len(bc.chain) == 1
    assert bc.chain[0].index == 0

    tx = {
        "tx_hash": "tx_123",
        "election_id": 1,
        "voter_hash": "voter_abc",
        "encrypted_vote": "enc_1",
        "timestamp": time.time(),
        "signature": "sig_1"
    }
    bc.add_transaction(tx)
    new_block = bc.mine_pending_transactions()
    
    assert new_block is not None
    assert new_block.index == 1
    assert len(bc.chain) == 2

    is_valid, msg = bc.is_chain_valid()
    assert is_valid is True
