import unittest
import time
import sys
import os

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.blockchain.cryptography import CryptoEngine
from backend.blockchain.block import Block, MerkleTree
from backend.blockchain.chain import Blockchain

class TestBlockchainEngine(unittest.TestCase):

    def test_crypto_engine_hashing(self):
        hash1 = CryptoEngine.sha256("test_data")
        hash2 = CryptoEngine.sha256("test_data")
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_ecdsa_signatures(self):
        priv, pub = CryptoEngine.generate_key_pair()
        data = "vote_payload_123"
        sig = CryptoEngine.sign_data(priv, data)
        self.assertGreaterThan(len(sig), 0) if hasattr(self, 'assertGreaterThan') else self.assertTrue(len(sig) > 0)
        self.assertTrue(CryptoEngine.verify_signature(pub, sig, data))
        self.assertFalse(CryptoEngine.verify_signature(pub, sig, "tampered_data"))

    def test_aes_vote_encryption(self):
        key = b"12345678901234567890123456789012"
        vote = "candidate_5"
        encrypted = CryptoEngine.encrypt_vote(vote, key)
        decrypted = CryptoEngine.decrypt_vote(encrypted, key)
        self.assertEqual(decrypted, vote)

    def test_merkle_tree(self):
        txs = [
            {"tx_hash": "hash1"},
            {"tx_hash": "hash2"},
            {"tx_hash": "hash3"}
        ]
        root = MerkleTree.compute_root(txs)
        self.assertEqual(len(root), 64)

    def test_blockchain_mining_and_validation(self):
        bc = Blockchain(difficulty=1)
        self.assertEqual(len(bc.chain), 1)
        self.assertEqual(bc.chain[0].index, 0)

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

        self.assertIsNotNone(new_block)
        self.assertEqual(new_block.index, 1)
        self.assertEqual(len(bc.chain), 2)

        is_valid, msg = bc.is_chain_valid()
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
