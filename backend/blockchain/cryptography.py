import os
import hashlib
import json
import base64
from typing import Dict, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature

class CryptoEngine:
    """
    Cryptographic utilities for SHA-256 hashing, ECDSA digital signatures, 
    and AES-256 GCM vote payload encryption.
    """

    @staticmethod
    def sha256(data: str) -> str:
        """Compute SHA-256 hex digest of input string."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_dict(data: Dict[str, Any]) -> str:
        """Deterministically compute SHA-256 digest of a dictionary."""
        sorted_json = json.dumps(data, sort_keys=True)
        return CryptoEngine.sha256(sorted_json)

    @staticmethod
    def generate_key_pair() -> Tuple[str, str]:
        """Generate ECDSA SECP256R1 private and public key pair in PEM format."""
        private_key = ec.generate_private_key(ec.SECP256R1())
        
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        pem_public = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        return pem_private, pem_public

    @staticmethod
    def sign_data(private_key_pem: str, data: str) -> str:
        """Sign a string message using ECDSA private key and SHA-256."""
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
        )
        signature = private_key.sign(
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def verify_signature(public_key_pem: str, signature_b64: str, data: str) -> bool:
        """Verify an ECDSA digital signature using the signer's public key."""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8')
            )
            signature = base64.b64decode(signature_b64)
            public_key.verify(
                signature,
                data.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except (InvalidSignature, Exception):
            return False

    @staticmethod
    def encrypt_vote(plain_vote: str, secret_key_32bytes: bytes) -> str:
        """Encrypt vote payload using AES-256 GCM."""
        aesgcm = AESGCM(secret_key_32bytes)
        nonce = os.urandom(12)
        encrypted_bytes = aesgcm.encrypt(nonce, plain_vote.encode('utf-8'), None)
        return base64.b64encode(nonce + encrypted_bytes).decode('utf-8')

    @staticmethod
    def decrypt_vote(encrypted_b64: str, secret_key_32bytes: bytes) -> str:
        """Decrypt vote payload using AES-256 GCM."""
        raw_data = base64.b64decode(encrypted_b64)
        nonce = raw_data[:12]
        ciphertext = raw_data[12:]
        aesgcm = AESGCM(secret_key_32bytes)
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_bytes.decode('utf-8')
