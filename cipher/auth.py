"""
Authentication and session management for Cipher Password Manager.
Handles master password verification, session state, and lockout logic.
"""

import time
from typing import Optional


MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 60  # seconds in seconds


# ============================================================================
# GLOBAL SESSION STATE (Singleton)
# ============================================================================

class Session:
    """Global session state for the current login."""
    
    def __init__(self):
        self.is_unlocked: bool = False
        self.aes_key: Optional[bytes] = None  # Wiped on lock/logout
        self.master_password_hash: str = ""


session = Session()


# ============================================================================
# LOGIN ATTEMPT LOCKOUT MANAGEMENT
# ============================================================================

_failed_attempts = 0
_lockout_until = 0.0


def record_failed_attempt() -> None:
    """Record a failed login attempt. Triggers lockout after MAX_ATTEMPTS."""
    global _failed_attempts, _lockout_until
    _failed_attempts += 1
    if _failed_attempts >= MAX_ATTEMPTS:
        _lockout_until = time.time() + LOCKOUT_DURATION


def is_locked_out() -> bool:
    """Check if login is currently locked due to failed attempts."""
    return time.time() < _lockout_until


def seconds_remaining() -> int:
    """Get number of seconds remaining in lockout period."""
    return max(0, int(_lockout_until - time.time()))


def reset_attempts() -> None:
    """Reset failed attempt counter and lockout timer."""
    global _failed_attempts, _lockout_until
    _failed_attempts = 0
    _lockout_until = 0.0


def get_attempts_remaining() -> int:
    """Get number of login attempts remaining before lockout."""
    return max(0, MAX_ATTEMPTS - _failed_attempts)


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def unlock_session(aes_key: bytes, master_password_hash: str) -> None:
    """
    Unlock the session after successful master password verification.
    
    Args:
        aes_key: The 32-byte AES-256 key derived from master password
        master_password_hash: Hash of the master password
    """
    session.is_unlocked = True
    session.aes_key = aes_key
    session.master_password_hash = master_password_hash
    reset_attempts()


def lock_session() -> None:
    """Lock the session and clear sensitive data."""
    session.is_unlocked = False
    session.aes_key = None  # CRITICAL: Wipe key from memory
    session.master_password_hash = ""
    reset_attempts()


def is_session_active() -> bool:
    """Check if user is currently logged in and vault is unlocked."""
    return session.is_unlocked and session.aes_key is not None
