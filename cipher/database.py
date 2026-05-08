"""
Database operations for Cipher Password Manager.
Manages SQLite connection and CRUD operations for vault and master config.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


DB_PATH = str(Path.home() / ".cipher" / "vault.db")


def ensure_db_exists():
    """Create .cipher directory and initialize database if it doesn't exist."""
    db_dir = Path.home() / ".cipher"
    db_dir.mkdir(exist_ok=True)
    
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Master config table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS master_config (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                pbkdf2_salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Vault credentials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                iv TEXT NOT NULL,
                tag TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()


def get_connection() -> sqlite3.Connection:
    """Get a new database connection."""
    ensure_db_exists()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================================
# MASTER CONFIG OPERATIONS
# ============================================================================

def set_master_password(password_hash: str, salt: str, pbkdf2_salt: str) -> None:
    """
    Store master password hash and salts. Creates new entry or updates existing.
    
    Args:
        password_hash: SHA-256 PBKDF2 hash (hex string)
        salt: Salt for password hashing (hex string)
        pbkdf2_salt: Salt for AES key derivation (hex string)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if master_config exists
    cursor.execute("SELECT id FROM master_config LIMIT 1")
    if cursor.fetchone():
        cursor.execute(
            "UPDATE master_config SET password_hash = ?, salt = ?, pbkdf2_salt = ?",
            (password_hash, salt, pbkdf2_salt)
        )
    else:
        cursor.execute(
            "INSERT INTO master_config (password_hash, salt, pbkdf2_salt) VALUES (?, ?, ?)",
            (password_hash, salt, pbkdf2_salt)
        )
    
    conn.commit()
    conn.close()


def get_master_password_config() -> Optional[Dict]:
    """
    Retrieve master password hash and salts.
    
    Returns:
        Dict with 'hash', 'salt', 'pbkdf2_salt' keys, or None if not set
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash, salt, pbkdf2_salt FROM master_config LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'hash': row[0],
            'salt': row[1],
            'pbkdf2_salt': row[2]
        }
    return None


def master_password_exists() -> bool:
    """Check if master password has been set."""
    return get_master_password_config() is not None


# ============================================================================
# VAULT OPERATIONS (CRUD)
# ============================================================================

def add_credential(website: str, username: str, encrypted_password: str,
                  iv: str, tag: str, notes: str = "") -> int:
    """
    Add a new credential to the vault.
    
    Args:
        website: Website/app name
        username: Username or email
        encrypted_password: AES-encrypted password (base64)
        iv: Initialization vector (base64)
        tag: Authentication tag (base64)
        notes: Optional notes
        
    Returns:
        ID of the newly inserted credential
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO vault 
           (website, username, encrypted_password, iv, tag, notes, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (website, username, encrypted_password, iv, tag, notes,
         datetime.now().isoformat(), datetime.now().isoformat())
    )
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return new_id


def get_all_credentials() -> List[Dict]:
    """
    Retrieve all credentials from vault.
    
    Returns:
        List of dicts with keys: id, website, username, encrypted_password, iv, tag, notes, created_at, updated_at
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vault ORDER BY website ASC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_credential(credential_id: int) -> Optional[Dict]:
    """
    Retrieve a single credential by ID.
    
    Args:
        credential_id: ID of the credential
        
    Returns:
        Dict with credential data or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vault WHERE id = ?", (credential_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def update_credential(credential_id: int, website: str, username: str,
                     encrypted_password: str, iv: str, tag: str,
                     notes: str = "") -> None:
    """
    Update an existing credential.
    
    Args:
        credential_id: ID of credential to update
        website: Website/app name
        username: Username or email
        encrypted_password: AES-encrypted password (base64)
        iv: Initialization vector (base64)
        tag: Authentication tag (base64)
        notes: Optional notes
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """UPDATE vault 
           SET website = ?, username = ?, encrypted_password = ?, iv = ?, tag = ?, notes = ?, updated_at = ?
           WHERE id = ?""",
        (website, username, encrypted_password, iv, tag, notes,
         datetime.now().isoformat(), credential_id)
    )
    
    conn.commit()
    conn.close()


def delete_credential(credential_id: int) -> None:
    """
    Delete a credential from the vault.
    
    Args:
        credential_id: ID of credential to delete
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM vault WHERE id = ?", (credential_id,))
    
    conn.commit()
    conn.close()


def search_credentials(query: str) -> List[Dict]:
    """
    Search credentials by website or username.
    
    Args:
        query: Search query string
        
    Returns:
        List of matching credentials
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    search_pattern = f"%{query}%"
    cursor.execute(
        """SELECT * FROM vault 
           WHERE website LIKE ? OR username LIKE ?
           ORDER BY website ASC""",
        (search_pattern, search_pattern)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_credential_count() -> int:
    """Get total number of credentials in vault."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM vault")
    count = cursor.fetchone()[0]
    conn.close()
    
    return count
