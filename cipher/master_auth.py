"""
Master authentication and recovery flows for Cipher Password Manager.
"""

import os
from typing import Optional, Tuple
from cryptography.exceptions import InvalidTag

import crypto
import database


RECOVERY_QUESTIONS = [
    "What was the name of your first school?",
    "What is your mother's maiden name?",
    "What was your childhood nickname?",
    "What is the name of your favorite teacher?",
    "What city were you born in?",
    "Custom question",
]


def hash_password(value: str, salt: bytes = None) -> tuple[str, str]:
    """Hash a password/answer with PBKDF2-SHA256."""
    return crypto.hash_password(value, salt)


def _normalize_answer(answer: str) -> str:
    return answer.strip().lower()


def _build_master_wrap_key(master_password: str, pbkdf2_salt_hex: str) -> bytes:
    return crypto.derive_key_from_secret(master_password, bytes.fromhex(pbkdf2_salt_hex))


def _build_recovery_wrap_key(answer: str, recovery_kdf_salt_hex: str) -> bytes:
    normalized = _normalize_answer(answer)
    return crypto.derive_key_from_secret(normalized, bytes.fromhex(recovery_kdf_salt_hex))


def _unwrap_vault_key_with_master(master_password: str, config: dict) -> bytes:
    # Legacy fallback: old scheme where vault key == derived key from master password.
    if not config.get('wrapped_vault_key_master'):
        return crypto.derive_aes_key(master_password, bytes.fromhex(config['pbkdf2_salt']))

    wrap_key = _build_master_wrap_key(master_password, config['pbkdf2_salt'])
    return crypto.decrypt_bytes(
        config['wrapped_vault_key_master'],
        config['wrapped_vault_key_master_iv'],
        config['wrapped_vault_key_master_tag'],
        wrap_key,
    )


def _unwrap_vault_key_with_recovery(answer: str, config: dict) -> bytes:
    wrap_key = _build_recovery_wrap_key(answer, config['recovery_kdf_salt'])
    return crypto.decrypt_bytes(
        config['wrapped_vault_key_recovery'],
        config['wrapped_vault_key_recovery_iv'],
        config['wrapped_vault_key_recovery_tag'],
        wrap_key,
    )


def _wrap_vault_key(vault_key: bytes, master_password: str, answer: str, pbkdf2_salt_hex: str, recovery_kdf_salt_hex: str):
    master_wrap_key = _build_master_wrap_key(master_password, pbkdf2_salt_hex)
    recovery_wrap_key = _build_recovery_wrap_key(answer, recovery_kdf_salt_hex)

    master_ct, master_iv, master_tag = crypto.encrypt_bytes(vault_key, master_wrap_key)
    rec_ct, rec_iv, rec_tag = crypto.encrypt_bytes(vault_key, recovery_wrap_key)

    return {
        'wrapped_vault_key_master': master_ct,
        'wrapped_vault_key_master_iv': master_iv,
        'wrapped_vault_key_master_tag': master_tag,
        'wrapped_vault_key_recovery': rec_ct,
        'wrapped_vault_key_recovery_iv': rec_iv,
        'wrapped_vault_key_recovery_tag': rec_tag,
    }


def setup_master_password(master_password: str, recovery_question: str, recovery_answer: str) -> Tuple[bool, str]:
    """First-time setup for master password and recovery data."""
    if not master_password or len(master_password) < 8:
        return False, "Master password must be at least 8 characters"

    if not recovery_question.strip():
        return False, "Recovery question is required"

    if not recovery_answer.strip():
        return False, "Recovery answer is required"

    password_hash, salt_hex = hash_password(master_password, os.urandom(32))
    recovery_hash, recovery_salt_hex = hash_password(_normalize_answer(recovery_answer), os.urandom(32))

    pbkdf2_salt_hex = os.urandom(32).hex()
    recovery_kdf_salt_hex = os.urandom(32).hex()
    vault_key = os.urandom(32)

    wrapped = _wrap_vault_key(
        vault_key,
        master_password,
        recovery_answer,
        pbkdf2_salt_hex,
        recovery_kdf_salt_hex,
    )

    database.set_master_password(
        password_hash,
        salt_hex,
        pbkdf2_salt_hex,
        recovery_question=recovery_question.strip(),
        recovery_answer_hash=recovery_hash,
        recovery_answer_salt=recovery_salt_hex,
        recovery_kdf_salt=recovery_kdf_salt_hex,
        wrapped_vault_key_master=wrapped['wrapped_vault_key_master'],
        wrapped_vault_key_master_iv=wrapped['wrapped_vault_key_master_iv'],
        wrapped_vault_key_master_tag=wrapped['wrapped_vault_key_master_tag'],
        wrapped_vault_key_recovery=wrapped['wrapped_vault_key_recovery'],
        wrapped_vault_key_recovery_iv=wrapped['wrapped_vault_key_recovery_iv'],
        wrapped_vault_key_recovery_tag=wrapped['wrapped_vault_key_recovery_tag'],
    )

    return True, "Master password created successfully"


def verify_master_password(master_password: str) -> bool:
    """Verify a user-entered master password."""
    config = database.get_master_password_config()
    if not config:
        return False

    return crypto.verify_master_password(master_password, config['hash'], config['salt'])


def get_vault_key_from_master_password(master_password: str) -> Optional[bytes]:
    """Resolve vault encryption key after successful master-password verification."""
    config = database.get_master_password_config()
    if not config:
        return None

    if not verify_master_password(master_password):
        return None

    try:
        return _unwrap_vault_key_with_master(master_password, config)
    except InvalidTag:
        return None


def get_recovery_question() -> Optional[str]:
    """Return configured recovery question, if present."""
    config = database.get_master_password_config()
    if not config:
        return None

    return config.get('recovery_question')


def reset_with_old_password(old_master_password: str, new_master_password: str) -> Tuple[bool, str]:
    """Reset master password using old master password verification."""
    if len(new_master_password) < 8:
        return False, "New password must be at least 8 characters"

    config = database.get_master_password_config()
    if not config:
        return False, "Master configuration not found"

    if not verify_master_password(old_master_password):
        return False, "Old master password is incorrect"

    try:
        vault_key = _unwrap_vault_key_with_master(old_master_password, config)
    except InvalidTag:
        return False, "Unable to unlock vault key with old password"

    new_hash, new_salt = hash_password(new_master_password, os.urandom(32))
    new_pbkdf2_salt_hex = os.urandom(32).hex()

    # Preserve existing recovery answer if available by requiring no changes to recovery fields.
    recovery_kdf_salt = config.get('recovery_kdf_salt')
    if recovery_kdf_salt and config.get('wrapped_vault_key_recovery'):
        # Rebuild master-wrapped key only, keep recovery wrap unchanged.
        master_wrap_key = _build_master_wrap_key(new_master_password, new_pbkdf2_salt_hex)
        master_ct, master_iv, master_tag = crypto.encrypt_bytes(vault_key, master_wrap_key)

        database.set_master_password(
            new_hash,
            new_salt,
            new_pbkdf2_salt_hex,
            wrapped_vault_key_master=master_ct,
            wrapped_vault_key_master_iv=master_iv,
            wrapped_vault_key_master_tag=master_tag,
        )
        return True, "Master password reset successfully"

    # Legacy fallback path.
    database.set_master_password(new_hash, new_salt, new_pbkdf2_salt_hex)
    return True, "Master password reset successfully"


def reset_with_security_question(answer: str, new_master_password: str) -> Tuple[bool, str]:
    """Reset master password using security-question recovery."""
    if len(new_master_password) < 8:
        return False, "New password must be at least 8 characters"

    config = database.get_master_password_config()
    if not config:
        return False, "Master configuration not found"

    if not config.get('recovery_answer_hash') or not config.get('recovery_answer_salt'):
        return False, "Security recovery is not configured for this vault"

    if not crypto.verify_password(_normalize_answer(answer), config['recovery_answer_hash'], config['recovery_answer_salt']):
        return False, "Recovery answer is incorrect"

    if not config.get('wrapped_vault_key_recovery') or not config.get('recovery_kdf_salt'):
        return False, "Security recovery cannot unlock existing vault key"

    try:
        vault_key = _unwrap_vault_key_with_recovery(answer, config)
    except InvalidTag:
        return False, "Unable to unlock vault key from recovery answer"

    new_hash, new_salt = hash_password(new_master_password, os.urandom(32))
    new_pbkdf2_salt_hex = os.urandom(32).hex()

    master_wrap_key = _build_master_wrap_key(new_master_password, new_pbkdf2_salt_hex)
    master_ct, master_iv, master_tag = crypto.encrypt_bytes(vault_key, master_wrap_key)

    database.set_master_password(
        new_hash,
        new_salt,
        new_pbkdf2_salt_hex,
        wrapped_vault_key_master=master_ct,
        wrapped_vault_key_master_iv=master_iv,
        wrapped_vault_key_master_tag=master_tag,
    )

    return True, "Master password reset successfully"
