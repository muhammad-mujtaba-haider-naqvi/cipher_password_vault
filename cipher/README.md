# Cipher — Password Manager

A modern, secure password manager built with Python and CustomTkinter. Stores all credentials behind a single master password with AES-256-GCM encryption.

## Features

### ✅ Tier 1 Core Features
1. **Password Strength Meter** — Real-time strength evaluation with zxcvbn (0-4 scale)
2. **Password Generator** — Cryptographically secure random generation with customizable options
3. **One-Click Copy + Auto-Clear** — Clipboard auto-clears after 30 seconds
4. **Search & Filter** — Live search across websites and usernames
5. **Login Attempt Lockout** — 3-attempt limit with 60-second lockout
6. **Auto-Lock on Idle** — Vault locks after 5 minutes of inactivity

### 🔐 Security
- **Master Password Hashing:** PBKDF2-SHA256 with 310,000 iterations
- **AES-256-GCM Encryption:** Authenticated encryption with random IVs
- **Key Derivation:** PBKDF2HMAC with 480,000 iterations
- **Session Management:** AES key wiped from memory on lock/logout
- **No Plaintext Storage:** Database stores only encrypted passwords

## Installation

### Prerequisites
- Python 3.11 or higher
- pip

### Setup

1. Clone/download the repository:
```bash
cd cipher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### First Time Setup
1. On first launch, you'll be prompted to create a **master password**
2. Choose a strong password (at least 8 characters, mix of uppercase, lowercase, digits, symbols)
3. Confirm the password and click **CREATE**

### Adding Credentials
1. Click **+ ADD** button
2. Fill in website/app name, username/email, and password
3. Use **⚡ Generate** to create a strong password
4. Add optional notes
5. Click **SAVE**

### Managing Credentials
- **View:** Credentials are listed in the vault
- **Search:** Use the search bar to filter by website or username
- **Edit:** Click the ✏️ icon to edit
- **Delete:** Click the 🗑️ icon to delete
- **Copy:** Click **📋 Copy** to copy password (auto-clears after 30s)

### Security Features
- **Auto-Lock:** Vault locks after 5 minutes of inactivity
- **Lockout:** 3 failed login attempts trigger 60-second lockout
- **Password Generator:** Use ⚡ to generate cryptographically secure passwords
- **Strength Meter:** Real-time password strength feedback

## File Structure

```
cipher/
├── main.py                  # Entry point
├── database.py              # SQLite operations
├── crypto.py                # Encryption/decryption
├── auth.py                  # Session management
├── generator.py             # Password generation
├── strength.py              # Password strength evaluation
├── clipboard_manager.py     # Clipboard operations
├── requirements.txt         # Dependencies
└── ui/
    ├── __init__.py
    ├── app.py               # Main window & navigation
    ├── login_screen.py      # Login UI
    ├── setup_screen.py      # Setup UI
    ├── vault_screen.py      # Vault display
    ├── add_edit_screen.py   # Credential form
    ├── generator_popup.py   # Password generator popup
    └── theme.py             # Colors & styling
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI | CustomTkinter 5.x |
| Database | SQLite3 |
| Encryption | AES-256-GCM (cryptography library) |
| Key Derivation | PBKDF2HMAC |
| Password Hashing | PBKDF2-SHA256 |
| Strength Meter | zxcvbn |
| Clipboard | pyperclip |
| Random Generation | secrets (built-in) |

## Security Notes

⚠️ **Important:**
- Your master password **cannot be recovered** if forgotten
- The database is stored in `~/.cipher/vault.db`
- Never share your master password
- The AES key is only stored in memory and is wiped on logout/lock
- Each password has a unique random IV (never reused)

## Development

### Testing Checklist

- [ ] Master password setup works
- [ ] Login with correct password succeeds
- [ ] Login with wrong password shows error + lockout after 3 attempts
- [ ] Lockout timer counts down correctly
- [ ] AES encryption/decryption round-trips correctly
- [ ] Password strength meter updates in real-time
- [ ] Password generator uses cryptographically secure randomness
- [ ] Copy button shows countdown and clears clipboard after 30s
- [ ] Search filters credentials by website/username
- [ ] Vault auto-locks after 5 minutes of inactivity
- [ ] Auto-lock clears AES key from memory
- [ ] All passwords can be successfully decrypted after retrieval

## License

This project is provided as-is for educational and personal use.
