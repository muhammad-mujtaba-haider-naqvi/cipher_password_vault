"""
Cipher Password Manager — Main Entry Point
A modern, secure password manager with AES-256-GCM encryption.
"""

import sys
import os

# Add the cipher package to the path if needed
if __name__ == "__main__":
    # If running directly, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from ui.app import main
    main()
