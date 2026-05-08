"""
Cryptographic utilities for Cipher Password Manager.
Handles master password hashing and AES-256-GCM encryption/decryption.
"""

import hashlib
import hmac
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# ============================================================================
# MASTER PASSWORD HASHING (SHA-256 with PBKDF2)
# ============================================================================

def hash_master_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """
    Hash master password using PBKDF2-SHA256.
    
    Args:
        password: Plain text master password
        salt: Optional salt bytes. If None, generates random 32-byte salt.
        
    Returns:
        Tuple of (hash_hex, salt_hex)
    """
    if salt is None:
        salt = os.urandom(32)
    
    # PBKDF2 with SHA256, 310,000 iterations (NIST 2023 recommendation)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        310000
    )
    return key.hex(), salt.hex()


def verify_master_password(password: str, stored_hash: str, salt_hex: str) -> bool:
    """
    Verify master password against stored hash using timing-safe comparison.
    
    Args:
        password: Plain text password to verify
        stored_hash: Stored hash hex string
        salt_hex: Stored salt hex string
        
    Returns:
        True if password matches, False otherwise
    """
    salt = bytes.fromhex(salt_hex)
    computed_hash, _ = hash_master_password(password, salt)
    return hmac.compare_digest(computed_hash, stored_hash)


# ============================================================================
# AES KEY DERIVATION (PBKDF2HMAC from master password)
# ============================================================================

def derive_aes_key(master_password: str, pbkdf2_salt: bytes) -> bytes:
    """
    Derive a 32-byte AES-256 key from the master password using PBKDF2HMAC.
    
    Args:
        master_password: Plain text master password
        pbkdf2_salt: Salt bytes for PBKDF2 derivation
        
    Returns:
        32-byte key suitable for AES-256
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=pbkdf2_salt,
        iterations=480000,
    )
    return kdf.derive(master_password.encode('utf-8'))


# ============================================================================
# AES-256-GCM ENCRYPTION / DECRYPTION
# ============================================================================

def encrypt_password(plaintext: str, aes_key: bytes) -> tuple[str, str, str]:
    """
    Encrypt a password using AES-256-GCM with a random IV.
    
    Args:
        plaintext: Plain text password to encrypt
        aes_key: 32-byte AES-256 key (from derive_aes_key)
        
    Returns:
        Tuple of (ciphertext_b64, iv_b64, tag_b64) all as base64-encoded strings
    """
    # Generate random 12-byte IV (nonce)
    iv = os.urandom(12)
    
    # Create cipher and encrypt
    aesgcm = AESGCM(aes_key)
    ciphertext_with_tag = aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)
    
    # Split ciphertext and authentication tag (last 16 bytes)
    ciphertext = ciphertext_with_tag[:-16]
    tag = ciphertext_with_tag[-16:]
    
    return (
        base64.b64encode(ciphertext).decode(),
        base64.b64encode(iv).decode(),
        base64.b64encode(tag).decode()
    )


def decrypt_password(ciphertext_b64: str, iv_b64: str, tag_b64: str, aes_key: bytes) -> str:
    """
    Decrypt a password using AES-256-GCM.
    
    Args:
        ciphertext_b64: Base64-encoded ciphertext
        iv_b64: Base64-encoded IV (nonce)
        tag_b64: Base64-encoded authentication tag
        aes_key: 32-byte AES-256 key
        
    Returns:
        Decrypted plain text password
        
    Raises:
        cryptography.exceptions.InvalidTag: If authentication check fails
    """
    # Decode from base64
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    tag = base64.b64decode(tag_b64)
    
    # Decrypt
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(iv, ciphertext + tag, None)
    
    return plaintext.decode('utf-8')
