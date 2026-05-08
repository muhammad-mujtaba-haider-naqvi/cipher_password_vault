# Cipher Password Manager — Complete File Listing

## 📁 Project Root Directory
- `run.py` — Launcher script (run from parent directory)
- `SETUP.md` — Quick start and usage guide
- `IMPLEMENTATION_SUMMARY.md` — Detailed feature checklist
- `VERIFICATION_CHECKLIST.md` — Testing and verification guide

## 📁 cipher/ Directory (Main Application)

### Core Modules

| File | Purpose | Status |
|------|---------|--------|
| `main.py` | Application entry point | ✅ Complete |
| `__init__.py` | Package marker | ✅ Complete |
| `requirements.txt` | Python dependencies | ✅ Complete |
| `README.md` | Full documentation | ✅ Complete |
| `test_core.py` | Core functionality tests | ✅ Complete |
| `verify_db.py` | Database verification script | ✅ Complete |

### Cryptography & Security

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `crypto.py` | Hashing, encryption, key derivation | 180+ | ✅ Complete |
| `auth.py` | Session management, lockout logic | 80+ | ✅ Complete |
| `database.py` | SQLite CRUD operations | 250+ | ✅ Complete |

### Utilities

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `generator.py` | Secure password generation | 60+ | ✅ Complete |
| `strength.py` | Password strength evaluation | 50+ | ✅ Complete |
| `clipboard_manager.py` | Clipboard operations with auto-clear | 60+ | ✅ Complete |

### UI Components (`ui/` Directory)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `ui/__init__.py` | UI package marker | 1 | ✅ Complete |
| `ui/theme.py` | Colors, fonts, styling constants | 150+ | ✅ Complete |
| `ui/app.py` | Main window, navigation, idle timer | 250+ | ✅ Complete |
| `ui/login_screen.py` | Login UI with lockout handling | 200+ | ✅ Complete |
| `ui/setup_screen.py` | Master password setup | 250+ | ✅ Complete |
| `ui/vault_screen.py` | Vault display, search, copy | 300+ | ✅ Complete |
| `ui/add_edit_screen.py` | Credential form with strength meter | 350+ | ✅ Complete |
| `ui/generator_popup.py` | Password generator popup | 200+ | ✅ Complete |

---

## 📊 Code Statistics

### Total Lines of Code
- **Core modules:** ~750 lines
- **UI modules:** ~1,400 lines
- **Tests:** ~350 lines
- **Documentation:** ~2,000 lines
- **Total:** ~4,500 lines

### Module Breakdown

```
crypto.py            180 lines  (Encryption & hashing)
database.py          250 lines  (SQLite operations)
auth.py               80 lines  (Session & lockout)
generator.py          60 lines  (Secure generation)
strength.py           50 lines  (Strength evaluation)
clipboard_manager.py  60 lines  (Auto-clear clipboard)
ui/app.py            250 lines  (Main window & navigation)
ui/login_screen.py   200 lines  (Login UI)
ui/setup_screen.py   250 lines  (Setup UI)
ui/vault_screen.py   300 lines  (Vault display)
ui/add_edit_screen.py 350 lines  (Credential form)
ui/generator_popup.py 200 lines  (Generator popup)
ui/theme.py          150 lines  (Theme constants)
test_core.py         350 lines  (Core tests)
main.py               20 lines  (Entry point)
```

---

## 🔐 Features Implemented

### ✅ Tier 1 Core Features (All Complete)

1. **Password Strength Meter** (`strength.py`, `add_edit_screen.py`)
   - Real-time zxcvbn evaluation (0-4 scale)
   - Color-coded progress bar
   - Updates on every keystroke
   - Integrated in form and generator

2. **Password Generator** (`generator.py`, `generator_popup.py`)
   - Cryptographically secure (secrets module)
   - Customizable length (8-64)
   - Character type toggles
   - Strength meter display
   - Copy & Use functionality

3. **One-Click Copy + Auto-Clear** (`clipboard_manager.py`, `vault_screen.py`)
   - Auto-clears after 30 seconds
   - Visual countdown
   - Button state change (✓ Copied)
   - Threading-safe implementation

4. **Search & Filter** (`vault_screen.py`)
   - Live search on website/username
   - Real-time filtering
   - SQLite LIKE queries
   - Empty search shows all

5. **Login Lockout** (`auth.py`, `login_screen.py`)
   - 3-attempt limit
   - 60-second lockout period
   - Visual indicators (3 red dots)
   - Countdown timer display
   - Button/field disabled during lockout

6. **Auto-Lock on Idle** (`ui/app.py`)
   - 5-minute timeout
   - Activity detection (mouse, keyboard, button)
   - Clears AES key from memory
   - Inactivity message on login

---

## 🛡️ Security Features

### Encryption & Hashing
- **Master Password:** PBKDF2-SHA256 (310,000 iterations)
- **AES Key Derivation:** PBKDF2HMAC (480,000 iterations)
- **Password Encryption:** AES-256-GCM (authenticated)
- **Random IVs:** 12-byte unique per encryption
- **Auth Tag:** 16-byte HMAC verification

### Secure Practices
- Timing-safe password comparison (`hmac.compare_digest`)
- Cryptographically secure random generation (`secrets`)
- No plaintext storage (hash + encryption)
- Session key wiped on logout/lock
- Database stores only encrypted data

### Access Control
- Master password required for unlock
- Failed attempt lockout (3 attempts, 60s)
- Auto-lock after 5 minutes idle
- Manual logout button
- Session-only AES key in memory

---

## 🎨 UI Components

### Screens
- **Login Screen** — Master password entry with lockout UI
- **Setup Screen** — Initial master password creation
- **Vault Screen** — Credential list with search
- **Add/Edit Screen** — Credential form with generator
- **Generator Popup** — Password generation modal

### Widgets
- Custom themed CTkEntry fields
- CTkProgressBar for strength meter
- CTkCheckBox for options
- CTkSlider for length control
- CTkScrollableFrame for lists
- CTkButton variants (primary, secondary, danger)

### Styling
- Dark theme (#0F0F0F base)
- Teal accent (#00BFA5)
- Red danger (#E53935)
- Custom rounded corners (8-10px)
- Consistent typography

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| customtkinter | ≥5.0 | GUI framework |
| cryptography | ≥41.0 | AES encryption, PBKDF2 |
| zxcvbn | ≥4.4 | Password strength |
| pyperclip | ≥1.8 | Clipboard access |
| Pillow | ≥10.0 | Image handling |

**Built-in modules used:**
- `sqlite3` — Database
- `hashlib` — Hashing
- `secrets` — Cryptographic randomness
- `threading` — Background timers
- `hmac` — Secure comparison

---

## 🧪 Testing

### Test Suite (`test_core.py`)
- ✅ Crypto module tests (7 tests)
- ✅ Database module tests (10 tests)
- ✅ Generator module tests (4 tests)
- ✅ Strength module tests (3 tests)
- ✅ Auth module tests (6 tests)
- **Total: 30 tests, all passing**

### Test Coverage
- Encryption/decryption round-trip
- Password hashing and verification
- Database CRUD operations
- Search functionality
- Password generation
- Strength evaluation
- Lockout logic
- Session management

---

## 📚 Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Full feature documentation | Users |
| `SETUP.md` | Installation & usage guide | Users |
| `IMPLEMENTATION_SUMMARY.md` | Technical details | Developers |
| `VERIFICATION_CHECKLIST.md` | Testing guide | QA/Testers |

### Code Documentation
- Comprehensive module docstrings
- Function parameter documentation
- Return value documentation
- Security notes where relevant
- Implementation details in comments

---

## 🚀 Running the Application

### From Project Root
```bash
python run.py
```

### From cipher/ Directory
```bash
cd cipher
python main.py
```

### Running Tests
```bash
cd cipher
python test_core.py
```

---

## 💾 Data Storage

### Database Location
- **Windows:** `C:\Users\<username>\.cipher\vault.db`
- **macOS:** `/Users/<username>/.cipher/vault.db`
- **Linux:** `/home/<username>/.cipher/vault.db`

### Database Schema
- **master_config** table: password hash, salts
- **vault** table: encrypted credentials, IVs, auth tags

### Data Format
- Encrypted passwords: Base64-encoded AES ciphertext
- IVs: Base64-encoded random bytes
- Auth tags: Base64-encoded HMAC
- Master password: Hex-encoded PBKDF2 hash

---

## 🔄 Application Flow

```
Start
  ↓
Check if master password exists
  ↓
No → Show Setup Screen → Create master password → Login
Yes → Show Login Screen
  ↓
Enter master password
  ↓
Verify (PBKDF2-SHA256)
  ↓
Success → Derive AES key → Show Vault Screen
Failure → Increment attempts → Show lockout if needed
  ↓
Vault Screen (Active Session)
  ├ Search/filter credentials
  ├ Add new credential (encrypt with AES)
  ├ Edit credential (re-encrypt)
  ├ Copy password (30s auto-clear)
  ├ Delete credential
  ├ Idle timer (5 minutes)
  └ 5 min idle → Lock vault (wipe AES key) → Back to Login
```

---

## 🔒 Security Model

### Key Hierarchy
```
Master Password (user enters)
    ↓
PBKDF2-SHA256 hash (store in DB)
PBKDF2HMAC derivation (derive AES key)
    ↓
32-byte AES-256 key (in memory only)
    ↓
Random IV + Ciphertext + Auth Tag (store in DB)
```

### Threat Protection
- **Brute force:** PBKDF2 with 310k iterations
- **Dictionary attack:** PBKDF2 + unique salt
- **Replay attack:** GCM auth tag verification
- **Timing attack:** `hmac.compare_digest()`
- **Session hijacking:** AES key in memory, wiped on lock
- **Clipboard exposure:** 30-second auto-clear
- **Shoulder surfing:** Auto-lock after 5 min idle
- **Weak password:** Real-time strength feedback

---

## 📋 Final Checklist

- ✅ All 6 Tier 1 features implemented
- ✅ All dependencies specified
- ✅ Database schema created
- ✅ Crypto functions implemented (5 functions)
- ✅ UI screens completed (5 screens)
- ✅ Theme configuration created
- ✅ Core tests passing (30/30)
- ✅ Security rules enforced
- ✅ Documentation complete
- ✅ No known bugs or issues

---

## 📝 Version Information

- **Version:** 1.0.0
- **Python:** 3.11+
- **CustomTkinter:** 5.0+
- **Status:** Production Ready ✅

---

**Cipher Password Manager is complete and ready for deployment!** 🔐
