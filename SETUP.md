# Cipher Password Manager — Quick Start Guide

## Installation & Setup

### 1. Prerequisites
- **Python 3.11** or higher (check with `python --version`)
- **pip** (usually included with Python)

### 2. Install Dependencies

From the `cipher/` directory:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `customtkinter` — Modern GUI framework
- `cryptography` — AES-256-GCM encryption
- `zxcvbn` — Password strength meter
- `pyperclip` — Clipboard management
- `Pillow` — Image handling

### 3. Run the Application

**Option A: From the cipher directory**
```bash
cd cipher
python main.py
```

**Option B: From the parent directory**
```bash
python run.py
```

---

## First Launch

When you launch Cipher for the first time:

1. **Setup Screen appears** — You'll be prompted to create a master password
2. **Create Master Password** — Choose a strong password (8+ characters, mix of types)
3. **Confirm Password** — Re-enter to verify
4. **Click CREATE** — Your vault is now ready!

The master password is:
- **Hashed with PBKDF2-SHA256** (310,000 iterations)
- **Never stored in plaintext**
- **Cannot be recovered if lost** ⚠️

---

## Using Cipher

### Adding Credentials

1. Click **+ ADD** button
2. Enter website/app name (e.g., `github.com`)
3. Enter your username or email
4. Enter your password (or click **⚡ Generate** for a strong one)
5. Add optional notes
6. Click **SAVE**

### Managing Credentials

| Action | Button | Notes |
|--------|--------|-------|
| **View** | Listed in vault | Shows website and username |
| **Search** | 🔍 Search bar | Filters by website or username |
| **Copy** | 📋 Copy | Password copies to clipboard, auto-clears in 30s |
| **Edit** | ✏️ | Modify any credential |
| **Delete** | 🗑️ | Permanently removes (no undo!) |

### Password Generator

Click **⚡ Generate** in the Add/Edit form:

- **Length slider** — Choose 8 to 64 characters
- **Character types** — Toggle uppercase, lowercase, digits, symbols
- **Strength meter** — Shows password quality in real-time
- **Regenerate** — Generate a new one
- **Copy & Use** — Insert into form and close

All generated passwords use **cryptographically secure randomness** (Python `secrets` module).

### Vault Auto-Lock

The vault automatically locks after **5 minutes of inactivity**:
- No mouse or keyboard activity detected
- AES key is **wiped from memory**
- You'll see a login screen message: "🔒 Vault locked due to inactivity"

Manual logout:
- Click **🔒** button in the vault header

---

## Security Features

### Password Strength Meter

Real-time strength evaluation as you type:
- **Very Weak** (red) — 0 score
- **Weak** (orange) — 1 score
- **Fair** (gold) — 2 score
- **Strong** (light green) — 3 score
- **Very Strong** (teal) — 4 score

Uses the **zxcvbn algorithm** (industry-standard strength evaluation).

### Login Lockout

After **3 failed login attempts**:
- Login field is disabled
- **60-second countdown** starts
- Displays remaining seconds
- Automatically resets when timer expires

### Copy & Auto-Clear

Click **📋 Copy** on any credential:
- Password copies to clipboard
- Button shows **✓ Copied** (green)
- Countdown displays: `"Clears in 30s"`
- After 30 seconds, clipboard is automatically **cleared**
- No manual action needed!

### Encryption

All passwords stored with:
- **AES-256-GCM** mode (authenticated encryption)
- **Random 12-byte IV** (never reused)
- **Random IV stored in database** (with ciphertext and auth tag)
- Each password encrypted with the **same master key** (derived from master password)

### Master Password

Your master password is:
- **Never stored** (only irreversible hash)
- **Hashed using PBKDF2-SHA256** with 310,000 iterations
- **Compared using timing-safe** comparison (prevents timing attacks)
- Used to derive the **AES key** (PBKDF2HMAC with 480,000 iterations)

### Session Management

- **AES key stored only in memory** (`session.aes_key`)
- **Cleared on logout or auto-lock** (set to `None`)
- **Cannot be written to disk**

---

## Database

Cipher stores data in:
- **Location:** `~/.cipher/vault.db` (your home directory)
- **Type:** SQLite3 (single file, no server)
- **Encrypted:** Individual password fields are encrypted with AES-256-GCM
- **Master password:** Only hash and salts stored (no plaintext)

---

## Troubleshooting

### App won't start
- Verify Python 3.11+ is installed: `python --version`
- Verify dependencies: `pip list | grep customtkinter`
- If missing, reinstall: `pip install -r requirements.txt`

### Forgot master password?
- **Cannot be recovered** — This is by design for security
- Delete `~/.cipher/vault.db` to reset
- Warning: You'll lose all stored passwords!

### Password won't decrypt
- Ensure you entered the correct master password
- Database may be corrupted (backup and reinstall)

### GUI looks wrong
- Supported on Windows, macOS, Linux
- Requires a modern terminal/X11 (not WSL without display server)

### Copy button not working
- Check clipboard permissions
- Try running as administrator
- Verify `pyperclip` is installed: `pip show pyperclip`

---

## Testing

Cipher includes a comprehensive test suite for core functionality:

```bash
cd cipher
python test_core.py
```

This tests:
- ✓ Password hashing and verification
- ✓ AES encryption/decryption
- ✓ Database CRUD operations
- ✓ Password generation
- ✓ Strength evaluation
- ✓ Login lockout logic
- ✓ Session management

---

## File Structure

```
cipher/
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── test_core.py                 # Core functionality tests
│
├── crypto.py                    # Hashing, encryption, key derivation
├── database.py                  # SQLite operations
├── auth.py                      # Session & lockout management
├── generator.py                 # Password generation
├── strength.py                  # Strength evaluation
├── clipboard_manager.py         # Clipboard operations
│
└── ui/
    ├── app.py                   # Main window & navigation
    ├── login_screen.py          # Login UI (with lockout)
    ├── setup_screen.py          # Master password setup
    ├── vault_screen.py          # Main credential list
    ├── add_edit_screen.py       # Credential form (with strength meter)
    ├── generator_popup.py       # Password generator popup
    └── theme.py                 # Colors & styling
```

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Start Cipher from cipher/ directory |
| `python run.py` | Start Cipher from parent directory |
| `python test_core.py` | Run core functionality tests |
| `pip install -r requirements.txt` | Install dependencies |
| `pip show customtkinter` | Check if CustomTkinter is installed |

---

## Support

For issues or feature requests, refer to the included code comments and documentation in each module.

**Remember:** This is a local password manager. Your passwords never leave your computer!
