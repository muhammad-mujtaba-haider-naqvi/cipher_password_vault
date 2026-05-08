"""
Login screen for Cipher Password Manager.
Handles master password entry, verification, and lockout UI.
"""

import customtkinter as ctk
from typing import Callable

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import crypto
import database
import auth
from ui import theme


class LoginScreen(ctk.CTkFrame):
    """Login screen with master password entry and lockout handling."""
    
    def __init__(self, parent, on_login_success: Callable, on_setup_needed: Callable, **kwargs):
        """
        Initialize login screen.
        
        Args:
            parent: Parent widget (root window)
            on_login_success: Callback when login succeeds (aes_key) -> None
            on_setup_needed: Callback when setup is needed () -> None
        """
        super().__init__(parent, **theme.get_main_frame_config(), **kwargs)
        
        self.on_login_success = on_login_success
        self.on_setup_needed = on_setup_needed
        self.lockout_timer_id = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and layout all UI elements."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY)
        main_container.pack(fill="both", expand=True, padx=theme.PADDING_XLARGE,
                           pady=theme.PADDING_XLARGE)
        
        # Title section
        title_frame = ctk.CTkFrame(main_container, fg_color=theme.BG_PRIMARY)
        title_frame.pack(pady=(0, theme.PADDING_XLARGE))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🔐  CIPHER",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_TITLE, "bold"),
            text_color=theme.ACCENT_PRIMARY
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Your vault. Your rules.",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(theme.PADDING_NORMAL, 0))
        
        # Lockout message (initially hidden)
        self.lockout_message = ctk.CTkLabel(
            main_container,
            text="🔒 Vault locked due to inactivity",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.WARNING_ORANGE
        )
        # Don't pack yet - only show when needed
        
        # Password input section
        input_frame = ctk.CTkFrame(main_container, fg_color=theme.BG_PRIMARY)
        input_frame.pack(pady=theme.PADDING_NORMAL, fill="x")
        
        label = ctk.CTkLabel(
            input_frame,
            text="Master Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        label.pack(anchor="w", pady=(0, theme.PADDING_SMALL))
        
        # Password entry with eye icon
        password_container = ctk.CTkFrame(input_frame, fg_color=theme.BG_PRIMARY)
        password_container.pack(fill="x")
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="Enter master password",
            show="*",
            **theme.get_input_config()
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())
        
        # Eye icon button
        self.eye_button = ctk.CTkButton(
            password_container,
            text="👁",
            width=45,
            height=theme.INPUT_HEIGHT,
            fg_color=theme.BG_SECONDARY,
            hover_color=theme.BG_TERTIARY,
            border_color=theme.BG_BORDER,
            border_width=1,
            font=(theme.FONT_FAMILY, 16),
            command=self._toggle_password_visibility,
            corner_radius=theme.CORNER_RADIUS
        )
        self.eye_button.pack(side="right", padx=(theme.PADDING_SMALL, 0))
        self.show_password = False
        
        # Attempt indicators and lockout message
        indicator_frame = ctk.CTkFrame(main_container, fg_color=theme.BG_PRIMARY)
        indicator_frame.pack(pady=theme.PADDING_NORMAL, fill="x")
        
        # Attempt dots
        dots_frame = ctk.CTkFrame(indicator_frame, fg_color=theme.BG_PRIMARY)
        dots_frame.pack(side="left")
        
        self.attempt_dots = []
        for i in range(auth.MAX_ATTEMPTS):
            dot = ctk.CTkLabel(
                dots_frame,
                text="●",
                font=(theme.FONT_FAMILY, 16),
                text_color=theme.DANGER_RED
            )
            dot.pack(side="left", padx=theme.PADDING_SMALL)
            self.attempt_dots.append(dot)
        
        # Remaining attempts text
        self.attempts_label = ctk.CTkLabel(
            indicator_frame,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.TEXT_SECONDARY
        )
        self.attempts_label.pack(side="left", padx=(theme.PADDING_NORMAL, 0))
        
        # Error message
        self.error_label = ctk.CTkLabel(
            main_container,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.DANGER_RED
        )
        self.error_label.pack(pady=(0, theme.PADDING_NORMAL))
        
        # Unlock button
        self.unlock_button = ctk.CTkButton(
            main_container,
            text="UNLOCK VAULT",
            command=self._attempt_login,
            **theme.get_button_primary_config(),
            width=300
        )
        self.unlock_button.pack(pady=theme.PADDING_NORMAL)
        
        # Setup link
        setup_frame = ctk.CTkFrame(main_container, fg_color=theme.BG_PRIMARY)
        setup_frame.pack(pady=(theme.PADDING_XLARGE, 0))
        
        setup_text = ctk.CTkLabel(
            setup_frame,
            text="First time?",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.TEXT_SECONDARY
        )
        setup_text.pack(side="left", padx=(0, theme.PADDING_SMALL))
        
        setup_button = ctk.CTkButton(
            setup_frame,
            text="Set master password",
            fg_color="transparent",
            text_color=theme.ACCENT_PRIMARY,
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            hover_color=theme.BG_SECONDARY,
            command=self.on_setup_needed,
            width=120,
            height=20
        )
        setup_button.pack(side="left")
        
        self._update_attempt_indicators()
    
    def _toggle_password_visibility(self):
        """Toggle password field visibility (show/hide)."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.eye_button.configure(text="👁‍🗨" if self.show_password else "👁")
    
    def _attempt_login(self):
        """Attempt to log in with entered password."""
        # Check if locked out
        if auth.is_locked_out():
            remaining = auth.seconds_remaining()
            self.error_label.configure(
                text=f"🔒 Locked for {remaining}s"
            )
            return
        
        password = self.password_entry.get()
        if not password:
            self.error_label.configure(text="Please enter your master password")
            return
        
        # Get master password config
        config = database.get_master_password_config()
        if not config:
            self.error_label.configure(text="Master password not set. Initialize first.")
            return
        
        # Verify password
        if not crypto.verify_master_password(password, config['hash'], config['salt']):
            auth.record_failed_attempt()
            remaining = auth.get_attempts_remaining()
            
            self.error_label.configure(
                text=f"❌ Incorrect password. {remaining} attempts remaining."
            )
            self._update_attempt_indicators()
            
            # Check if now locked out
            if auth.is_locked_out():
                self.unlock_button.configure(state="disabled")
                self.password_entry.configure(state="disabled")
                self._start_lockout_timer()
            
            self.password_entry.delete(0, "end")
            return
        
        # Successful login!
        self.error_label.configure(text="")
        self.password_entry.delete(0, "end")
        
        # Derive AES key
        pbkdf2_salt = bytes.fromhex(config['pbkdf2_salt'])
        aes_key = crypto.derive_aes_key(password, pbkdf2_salt)
        
        # Update session
        auth.unlock_session(aes_key, config['hash'])
        
        # Callback
        self.on_login_success()
    
    def _update_attempt_indicators(self):
        """Update the visual attempt indicator dots and text."""
        remaining = auth.get_attempts_remaining()
        
        # Update dots - fade out used attempts
        used = auth.MAX_ATTEMPTS - remaining
        for i, dot in enumerate(self.attempt_dots):
            if i < used:
                dot.configure(text_color="#555555")  # Faded
            else:
                dot.configure(text_color=theme.DANGER_RED)
        
        if remaining == auth.MAX_ATTEMPTS:
            self.attempts_label.configure(text="")
        else:
            self.attempts_label.configure(
                text=f"{remaining} attempts remaining"
            )
    
    def _start_lockout_timer(self):
        """Start countdown timer for lockout."""
        def countdown():
            if auth.is_locked_out():
                remaining = auth.seconds_remaining()
                self.error_label.configure(text=f"🔒 Locked for {remaining}s")
                self.lockout_timer_id = self.after(1000, countdown)
            else:
                # Lockout expired
                self.unlock_button.configure(state="normal")
                self.password_entry.configure(state="normal")
                self.error_label.configure(text="")
                self._update_attempt_indicators()
                self.password_entry.focus()
        
        countdown()
    
    def show_inactivity_message(self):
        """Show inactivity lockout message."""
        self.lockout_message.pack(pady=(0, theme.PADDING_NORMAL))
        self.after(5000, lambda: self.lockout_message.pack_forget())
    
    def on_show(self):
        """Called when screen is shown. Reset UI state."""
        self.password_entry.delete(0, "end")
        self.error_label.configure(text="")
        self._update_attempt_indicators()
        self.password_entry.focus()
