# Cipher Password Manager — Verification Checklist

Use this checklist to verify that Cipher is functioning correctly.

## ✓ Installation Verification

- [ ] Python 3.11+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r cipher/requirements.txt`
- [ ] No errors during dependency installation
- [ ] All files present in `cipher/` directory (see File Structure in README.md)

## ✓ Core Functionality Tests

Run the test suite first:
```bash
cd cipher
python test_core.py
```

Verify output shows:
- [ ] ✓ All crypto tests pass
- [ ] ✓ All database tests pass
- [ ] ✓ All generator tests pass
- [ ] ✓ All strength tests pass
- [ ] ✓ All auth tests pass
- [ ] ✓ "ALL TESTS PASSED" message appears

## ✓ Application Launch

- [ ] Application starts without errors: `python main.py` (from cipher/) or `python run.py` (from parent)
- [ ] Window title shows "Cipher"
- [ ] Dark theme loads correctly
- [ ] No console errors during startup

## ✓ Setup Screen (First Time)

- [ ] Setup screen appears on first launch
- [ ] Warning message shows: "⚠️ This password cannot be recovered if forgotten"
- [ ] Eye icon toggles password visibility
- [ ] Strength meter shows real-time feedback (color + label)
- [ ] "Very Weak" → "Very Strong" range works
- [ ] CREATE button is clickable
- [ ] Passwords must match to proceed
- [ ] Password must be 8+ characters

## ✓ Master Password Setup

- [ ] Setup with: password="Test123!@" confirm="Test123!@"
- [ ] Click CREATE
- [ ] Application transitions to Login Screen
- [ ] No errors in console

## ✓ Login Screen

- [ ] Login screen appears with:
  - [ ] 🔐 CIPHER title
  - [ ] "Your vault. Your rules." subtitle
  - [ ] Master Password input field
  - [ ] Eye icon for visibility toggle
  - [ ] Attempt dots (● ● ●) showing
  - [ ] UNLOCK VAULT button
  - [ ] "First time? Set master password" link

## ✓ Login Functionality

### Correct Password
- [ ] Enter correct master password
- [ ] Press Enter or click UNLOCK VAULT
- [ ] Vault screen appears immediately
- [ ] No error message shown

### Wrong Password
- [ ] Enter wrong password
- [ ] Click UNLOCK VAULT
- [ ] Error shows: "❌ Incorrect password. X attempts remaining."
- [ ] Attempt dots fade (first one becomes grayed)
- [ ] Field clears
- [ ] Can try again

### Lockout (3 Failures)
- [ ] Enter wrong password 3 times
- [ ] After 3rd failure, button disables
- [ ] Password field disables
- [ ] Countdown starts: "🔒 Locked for 60s"
- [ ] Countdown decrements to 0
- [ ] After timeout, button/field re-enable
- [ ] Can log in again

## ✓ Vault Screen

- [ ] Shows: 🔐 CIPHER title
- [ ] Search bar with 🔍 icon
- [ ] + ADD button (teal)
- [ ] 🔒 logout button
- [ ] Scrollable vault list
- [ ] Footer shows: "0 entries stored" (empty initially)

## ✓ Add Credential Form

Click + ADD:

- [ ] Form opens with title "Add New Credential"
- [ ] Fields visible:
  - [ ] Website / App Name
  - [ ] Username / Email
  - [ ] Password (with 👁 eye icon and ⚡ Generate button)
  - [ ] Notes (optional)
- [ ] Password strength meter below password field
- [ ] CANCEL and SAVE buttons at bottom
- [ ] All input fields have proper styling (dark theme)

## ✓ Password Generator Popup

Click ⚡ Generate:

- [ ] Popup window opens
- [ ] Title: "⚡ Generate Password"
- [ ] Length slider (8-64) with current value displayed
- [ ] 4 checkboxes:
  - [ ] Uppercase (A-Z) — checked
  - [ ] Lowercase (a-z) — checked
  - [ ] Digits (0-9) — checked
  - [ ] Symbols (!@#$%...) — checked
- [ ] Generated password displayed in read-only field
- [ ] Strength meter for generated password
- [ ] 🔄 Regenerate button
- [ ] ✓ Copy & Use button

Test generator:
- [ ] Adjust length slider → password regenerates
- [ ] Uncheck "Symbols" → regenerates without symbols
- [ ] Click Regenerate → new password appears
- [ ] Click Copy & Use → closes popup, password in form

## ✓ Strength Meter

In Add/Edit form, test strength meter:

- [ ] Type "123456" → "Very Weak" (red)
- [ ] Type "password123" → "Weak" or "Fair"
- [ ] Type "Test123!@#$Secure" → "Strong" or "Very Strong"
- [ ] Color changes with score
- [ ] Updates on every keystroke
- [ ] Meter bar fills 0-100% based on strength

## ✓ Add Credential

- [ ] Fill in:
  - Website: `github.com`
  - Username: `user@example.com`
  - Password: `Test123!@#Secure`
  - Notes: `My GitHub account`
- [ ] Click SAVE
- [ ] Form closes, returns to vault
- [ ] Credential appears in list:
  - [ ] Shows: 🌐 github.com
  - [ ] Shows: user@example.com
  - [ ] 📋 Copy button
  - [ ] ✏️ Edit button
  - [ ] 🗑️ Delete button

## ✓ Copy Button

- [ ] Click 📋 Copy on credential
- [ ] Button changes to ✓ Copied (green text)
- [ ] Countdown appears: "Clears in 30s"
- [ ] Countdown decrements: 29s, 28s, ...
- [ ] At 0s, button resets to 📋 Copy, countdown disappears
- [ ] Verify password is in clipboard (paste test):
  - [ ] Open Notepad/text editor
  - [ ] Paste (Ctrl+V)
  - [ ] Should show: `Test123!@#Secure`
- [ ] After 30s, paste again
  - [ ] Should be empty or show nothing

## ✓ Search Functionality

- [ ] Add 2-3 more credentials (different websites)
- [ ] Click search bar
- [ ] Type "github"
  - [ ] Only github.com credential shows
  - [ ] Others disappear
- [ ] Clear search
  - [ ] All credentials reappear
- [ ] Type "user"
  - [ ] Only credentials with "user" in username show
- [ ] Clear search
  - [ ] All credentials reappear
- [ ] Footer shows correct count

## ✓ Edit Credential

- [ ] Click ✏️ Edit on a credential
- [ ] Form opens with title "Edit Credential"
- [ ] All fields pre-filled with credential data
- [ ] Password field shows ••••• (hidden)
- [ ] Click 👁 eye → password visible
- [ ] Modify a field
- [ ] Click SAVE
- [ ] Changes appear in vault list

## ✓ Delete Credential

- [ ] Click 🗑️ Delete on a credential
- [ ] Confirmation dialog appears:
  - [ ] Message: "Delete this credential? This cannot be undone."
  - [ ] Cancel and Delete buttons
- [ ] Click Delete
  - [ ] Dialog closes
  - [ ] Credential disappears from list
  - [ ] Count decrements
- [ ] Click Cancel
  - [ ] Dialog closes, credential remains

## ✓ Auto-Lock on Idle

This feature requires patience (5 minutes). To test quickly:
- [ ] Edit `ui/app.py` — Change `IDLE_TIMEOUT = 300` to `IDLE_TIMEOUT = 10` (10 seconds)
- [ ] Rebuild and run
- [ ] Credentials must be visible in vault
- [ ] Don't touch mouse or keyboard for 10 seconds
- [ ] Vault screen should disappear
- [ ] Login screen should appear
- [ ] Banner message should show: "🔒 Vault locked due to inactivity"
- [ ] Message fades after 5 seconds
- [ ] AES key should be cleared from memory (can't decrypt without re-login)

## ✓ Logout

- [ ] Click 🔒 logout button in vault header
- [ ] Vault closes immediately
- [ ] Login screen appears
- [ ] No inactivity message (this is manual logout)
- [ ] Can log in again with master password

## ✓ Database

Check database file location:
- [ ] On Windows: `C:\Users\<your-username>\.cipher\vault.db` exists
- [ ] On Mac: `~/.cipher/vault.db` exists
- [ ] File size should be >10 KB (with credentials)
- [ ] File is SQLite (can open with SQLite tools)
- [ ] Database persists between app restarts

## ✓ Security Verification

### Master Password Never Plaintext
- [ ] Open `~/.cipher/vault.db` with SQLite viewer
- [ ] Look at `master_config` table
- [ ] password_hash column shows hex hash (not readable)
- [ ] No plaintext master password visible

### Each Password Encrypted
- [ ] In `vault` table, look at `encrypted_password` column
- [ ] Shows base64 text (gibberish, not plaintext)
- [ ] Cannot read actual password from database
- [ ] `iv` and `tag` columns also present (required for AES-GCM)

### IV is Random
- [ ] Add same password twice to two credentials
- [ ] In database, look at `iv` column
- [ ] Each entry has different IV value
- [ ] IVs are base64-encoded

## ✓ Edge Cases

### Empty Fields
- [ ] Try to save credential with empty website → Error: "Website/App name is required"
- [ ] Try to save credential with empty username → Error: "Username/Email is required"
- [ ] Try to save credential with empty password → Error: "Password is required"

### Long Input
- [ ] Add credential with:
  - Website: 100-character string
  - Username: 100-character string
  - Password: 100-character string
  - Notes: 500-character string
- [ ] Should save and display correctly

### Special Characters
- [ ] Add credential with:
  - Website: `example@sub.com:8080`
  - Username: `user+tag@example.com`
  - Password: `!@#$%^&*()_+-=[]{}|;:,.<>?`
- [ ] Should save and decrypt correctly

### Search Edge Cases
- [ ] Search for uppercase: "GITHUB"
- [ ] Should find "github.com" (case-insensitive)
- [ ] Search for partial: "git"
- [ ] Should find "github.com"
- [ ] Search for special char: "@"
- [ ] Should find credentials with @ in username

## ✓ Performance

- [ ] App starts in <2 seconds
- [ ] GUI responds instantly to clicks
- [ ] Search filters in real-time (no lag)
- [ ] Strength meter updates smoothly on typing
- [ ] No hanging or freezing

## ✓ Visual Design

- [ ] Dark theme throughout (no bright white backgrounds)
- [ ] Teal accent color (#00BFA5) on primary buttons and title
- [ ] Red color (#E53935) on errors and dangerous actions
- [ ] Text is readable (white on dark background)
- [ ] Buttons have hover effects
- [ ] Rounded corners on input fields and buttons
- [ ] Icons are clearly visible and appropriately placed

## ✓ Error Handling

- [ ] Close app during idle countdown → No crash
- [ ] Rapidly click buttons → No duplicate actions
- [ ] Fill form, click Cancel → Returns to vault safely
- [ ] Delete credential while viewing → Updates correctly
- [ ] Network interruption (N/A - local only)

## ✓ Multi-Launch

- [ ] Close and reopen app
- [ ] Master password setup not required (already exists)
- [ ] Login screen appears immediately
- [ ] All previously added credentials are still there
- [ ] Can log in and view credentials

---

## Summary

If all items are checked ✓, Cipher Password Manager is **fully functional and ready to use!**

### Quick Checklist for Daily Use

Every time you use Cipher, verify:
- [ ] App starts without errors
- [ ] Login works with master password
- [ ] Credentials are displayed in vault
- [ ] Passwords decrypt correctly
- [ ] Copy button works
- [ ] Search filters credentials
- [ ] Logout clears the vault

---

**Congratulations! Cipher is ready for secure password management!** 🔐
