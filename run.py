#!/usr/bin/env python3
"""
Cipher Password Manager Launcher
Run from the IS-Project directory: python run.py
"""

import sys
import os

# Add cipher directory to path
cipher_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cipher')
sys.path.insert(0, cipher_dir)

from ui.app import main

if __name__ == "__main__":
    main()
