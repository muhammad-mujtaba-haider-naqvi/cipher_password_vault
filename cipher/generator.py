"""
Password generation utilities for Cipher Password Manager.
Uses cryptographically secure random generation (secrets module).
"""

import secrets
import string
from typing import Optional


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True
) -> str:
    """
    Generate a cryptographically secure random password.
    
    Uses the `secrets` module for cryptographic randomness.
    Ensures at least one character from each selected type is included.
    
    Args:
        length: Total password length (8-64 recommended)
        use_upper: Include uppercase letters (A-Z)
        use_lower: Include lowercase letters (a-z)
        use_digits: Include digits (0-9)
        use_symbols: Include symbols (!@#$%^&*...)
        
    Returns:
        Generated password string
        
    Raises:
        ValueError: If length < 1 or no character types selected
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")
    
    charset = ""
    required = []
    
    # Build character set and ensure at least one from each selected type
    if use_upper:
        charset += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    
    if use_lower:
        charset += string.ascii_lowercase
        required.append(secrets.choice(string.ascii_lowercase))
    
    if use_digits:
        charset += string.digits
        required.append(secrets.choice(string.digits))
    
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        charset += symbols
        required.append(secrets.choice(symbols))
    
    if not charset:
        raise ValueError("At least one character type must be selected")
    
    # Generate remaining characters
    remaining_length = length - len(required)
    if remaining_length < 0:
        raise ValueError(f"Length {length} is too short for selected character types")
    
    remaining = [secrets.choice(charset) for _ in range(remaining_length)]
    
    # Combine required and remaining characters
    password_list = required + remaining
    
    # Shuffle using cryptographically secure shuffle
    secrets.SystemRandom().shuffle(password_list)
    
    return ''.join(password_list)
