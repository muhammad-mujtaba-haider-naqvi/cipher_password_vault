"""
Test script for Cipher Password Manager core functionality.
Tests encryption, hashing, database operations, and password generation.
Does NOT test GUI components.
"""

import sys
import os

# Add the cipher directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crypto import (
    hash_master_password, verify_master_password,
    derive_aes_key, encrypt_password, decrypt_password
)
from database import (
    ensure_db_exists, set_master_password, get_master_password_config,
    add_credential, get_all_credentials, get_credential,
    update_credential, delete_credential, search_credentials
)
from generator import generate_password
from strength import evaluate_password_strength
from auth import (
    record_failed_attempt, is_locked_out, get_attempts_remaining,
    reset_attempts, unlock_session, lock_session, is_session_active
)
from master_auth import (
    setup_master_password,
    verify_master_password as verify_master_password_flow,
    reset_with_old_password,
    reset_with_security_question,
)

def test_crypto():
    """Test cryptographic functions."""
    print("\n=== Testing Crypto Module ===")
    
    # Test master password hashing
    password = "TestPassword123!"
    password_hash, salt = hash_master_password(password)
    print(f"✓ Master password hashed: {password_hash[:16]}...")
    
    # Test password verification
    assert verify_master_password(password, password_hash, salt), "Password verification failed"
    print("✓ Password verification works")
    
    assert not verify_master_password("WrongPassword", password_hash, salt), "Should reject wrong password"
    print("✓ Wrong password correctly rejected")
    
    # Test AES key derivation
    pbkdf2_salt = os.urandom(32)
    aes_key = derive_aes_key(password, pbkdf2_salt)
    assert len(aes_key) == 32, f"Expected 32-byte key, got {len(aes_key)}"
    print(f"✓ AES key derived: {len(aes_key)} bytes")
    
    # Test encryption/decryption
    plaintext = "MySecretPassword123"
    ciphertext, iv, tag = encrypt_password(plaintext, aes_key)
    print(f"✓ Password encrypted")
    
    decrypted = decrypt_password(ciphertext, iv, tag, aes_key)
    assert decrypted == plaintext, f"Expected '{plaintext}', got '{decrypted}'"
    print(f"✓ Password decrypted correctly")
    
    # Test that different IVs produce different ciphertexts
    ciphertext2, iv2, tag2 = encrypt_password(plaintext, aes_key)
    assert iv != iv2, "IVs should be different"
    print("✓ Different IVs generated for same plaintext")

def test_database():
    """Test database operations."""
    print("\n=== Testing Database Module ===")
    
    # Ensure DB exists
    ensure_db_exists()
    print("✓ Database initialized")
    
    # Set master password (used by other tests)
    password = "TestMasterPass123!"
    password_hash, salt = hash_master_password(password)
    pbkdf2_salt = os.urandom(32)
    set_master_password(password_hash, salt, pbkdf2_salt.hex())
    print("✓ Master password stored")
    
    # Get master password config
    config = get_master_password_config()
    assert config is not None, "Failed to retrieve master password config"
    print("✓ Master password config retrieved")
    
    # Add credentials
    aes_key = derive_aes_key(password, pbkdf2_salt)
    ciphertext, iv, tag = encrypt_password("password123", aes_key)
    
    cred_id = add_credential("github.com", "user@example.com", ciphertext, iv, tag, "My GitHub account")
    assert cred_id > 0, "Failed to add credential"
    print(f"✓ Credential added (ID: {cred_id})")
    
    # Get credential
    cred = get_credential(cred_id)
    assert cred is not None, "Failed to retrieve credential"
    assert cred['website'] == "github.com", "Website mismatch"
    print("✓ Credential retrieved")
    
    # Get all credentials
    all_creds = get_all_credentials()
    assert len(all_creds) > 0, "No credentials found"
    print(f"✓ Retrieved {len(all_creds)} credential(s)")
    
    # Search credentials
    results = search_credentials("github")
    assert len(results) > 0, "Search failed"
    print(f"✓ Search found {len(results)} matching credential(s)")
    
    # Update credential
    ciphertext2, iv2, tag2 = encrypt_password("newpassword456", aes_key)
    update_credential(cred_id, "github.com", "newemail@example.com", ciphertext2, iv2, tag2, "Updated note")
    print("✓ Credential updated")
    
    # Verify update
    updated_cred = get_credential(cred_id)
    assert updated_cred['username'] == "newemail@example.com", "Update verification failed"
    print("✓ Update verified")
    
    # Delete credential
    delete_credential(cred_id)
    deleted_cred = get_credential(cred_id)
    assert deleted_cred is None, "Credential was not deleted"
    print("✓ Credential deleted")

def test_generator():
    """Test password generation."""
    print("\n=== Testing Password Generator ===")
    
    # Generate password with defaults
    pwd = generate_password()
    assert len(pwd) == 16, f"Expected 16 chars, got {len(pwd)}"
    print(f"✓ Generated 16-char password")
    
    # Generate with custom length
    pwd_long = generate_password(length=32)
    assert len(pwd_long) == 32, f"Expected 32 chars, got {len(pwd_long)}"
    print(f"✓ Generated 32-char password")
    
    # Generate with limited character types
    pwd_alpha = generate_password(use_digits=False, use_symbols=False)
    assert pwd_alpha.isalpha(), "Should only contain letters"
    print("✓ Generated alphabetic-only password")
    
    # Verify cryptographic randomness (generate 3 and verify they're different)
    pwd1 = generate_password()
    pwd2 = generate_password()
    pwd3 = generate_password()
    assert pwd1 != pwd2 != pwd3, "Generated passwords should be unique"
    print("✓ Generated passwords are cryptographically unique")

def test_strength():
    """Test password strength evaluation."""
    print("\n=== Testing Strength Meter ===")
    
    weak_pwd = "123456"
    weak_result = evaluate_password_strength(weak_pwd)
    assert weak_result['score'] < 2, "Weak password should have low score"
    print(f"✓ Weak password scored: {weak_result['label']} ({weak_result['score']})")
    
    strong_pwd = "P@ssw0rd!Secure#2024"
    strong_result = evaluate_password_strength(strong_pwd)
    assert strong_result['score'] >= 3, "Strong password should have high score"
    print(f"✓ Strong password scored: {strong_result['label']} ({strong_result['score']})")
    
    # Verify color mapping
    assert 'color' in strong_result, "Color should be in result"
    print(f"✓ Color assigned: {strong_result['color']}")

def test_auth():
    """Test authentication and lockout logic."""
    print("\n=== Testing Auth Module ===")
    
    # Reset attempts
    reset_attempts()
    assert get_attempts_remaining() == 3, "Should start with 3 attempts"
    print("✓ Attempts reset to 3")
    
    # Record failed attempts
    record_failed_attempt()
    assert get_attempts_remaining() == 2, "Should have 2 attempts left"
    print("✓ Failed attempt recorded")
    
    record_failed_attempt()
    assert get_attempts_remaining() == 1, "Should have 1 attempt left"
    
    record_failed_attempt()
    assert get_attempts_remaining() == 0, "Should have 0 attempts left"
    assert is_locked_out(), "Should be locked out after 3 failures"
    print("✓ Lockout triggered after 3 failures")
    
    reset_attempts()
    assert not is_locked_out(), "Should not be locked out after reset"
    print("✓ Lockout reset works")
    
    # Test session management
    assert not is_session_active(), "Session should not be active initially"
    aes_key = os.urandom(32)
    unlock_session(aes_key, "hash123")
    assert is_session_active(), "Session should be active after unlock"
    print("✓ Session unlocked")
    
    lock_session()
    assert not is_session_active(), "Session should not be active after lock"
    print("✓ Session locked")


def test_master_auth_recovery():
    """Test first-time setup and both recovery reset paths."""
    print("\n=== Testing Master Auth Recovery Flows ===")

    success, message = setup_master_password(
        "InitPass!234",
        "What city were you born in?",
        "Lahore"
    )
    assert success, f"Setup should succeed: {message}"
    print("✓ First-time setup with recovery succeeded")

    assert verify_master_password_flow("InitPass!234"), "Initial password verification failed"
    print("✓ Master password verification works")

    success, message = reset_with_old_password("InitPass!234", "ChangedPass!234")
    assert success, f"Reset with old password should succeed: {message}"
    assert verify_master_password_flow("ChangedPass!234"), "Password should verify after old-password reset"
    print("✓ Reset with old master password works")

    success, message = reset_with_security_question("Lahore", "RecoveredPass!234")
    assert success, f"Reset with security question should succeed: {message}"
    assert verify_master_password_flow("RecoveredPass!234"), "Password should verify after security reset"
    print("✓ Reset with security question works")

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("CIPHER PASSWORD MANAGER — CORE FUNCTIONALITY TESTS")
    print("=" * 60)
    
    try:
        test_crypto()
        test_database()
        test_generator()
        test_strength()
        test_auth()
        test_master_auth_recovery()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
