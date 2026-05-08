"""
Add/Edit credential screen for Cipher Password Manager.
Form for entering new credentials with password strength meter and generator.
"""

import customtkinter as ctk
from typing import Callable, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
import auth
import crypto
import strength
from ui import theme


class AddEditScreen(ctk.CTkFrame):
    """Form to add or edit a credential."""
    
    def __init__(self, parent, on_save: Callable, on_cancel: Callable, on_generate: Callable, **kwargs):
        """
        Initialize add/edit screen.
        
        Args:
            parent: Parent widget
            on_save: Callback when save succeeds (credential_id) -> None
            on_cancel: Callback when cancel is clicked () -> None
            on_generate: Callback to open generator popup (entry_widget, strength_callback) -> None
        """
        super().__init__(parent, **theme.get_main_frame_config(), **kwargs)
        
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_generate = on_generate
        
        self.credential_id: Optional[int] = None
        self.is_editing = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout form elements."""
        # Main container
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.BG_PRIMARY
        )
        container.pack(fill="both", expand=True, padx=theme.PADDING_XLARGE,
                      pady=theme.PADDING_XLARGE)
        
        # Title
        self.title_label = ctk.CTkLabel(
            container,
            text="Add New Credential",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_XLARGE, "bold"),
            text_color=theme.TEXT_PRIMARY
        )
        self.title_label.pack(anchor="w", pady=(0, theme.PADDING_XLARGE))
        
        # Website field
        self._create_field(container, "Website / App Name", "e.g. github.com")
        self.website_entry = self._last_entry
        
        # Username field
        self._create_field(container, "Username / Email", "")
        self.username_entry = self._last_entry
        
        # Password field with generator button
        password_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        password_frame.pack(fill="x", pady=theme.PADDING_NORMAL)
        
        label_frame = ctk.CTkFrame(password_frame, fg_color=theme.BG_PRIMARY)
        label_frame.pack(anchor="w", pady=(0, theme.PADDING_SMALL))
        
        label = ctk.CTkLabel(
            label_frame,
            text="Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        label.pack(side="left")
        
        gen_button = ctk.CTkButton(
            label_frame,
            text="⚡ Generate",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            fg_color="transparent",
            text_color=theme.ACCENT_PRIMARY,
            hover_color=theme.BG_SECONDARY,
            width=80,
            height=20,
            command=self._open_generator
        )
        gen_button.pack(side="right")
        
        # Password entry
        password_container = ctk.CTkFrame(password_frame, fg_color=theme.BG_PRIMARY)
        password_container.pack(fill="x")
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="",
            show="*",
            **theme.get_input_config()
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.bind("<KeyRelease>", self._update_strength_meter)
        
        # Eye icon
        self.password_eye_button = ctk.CTkButton(
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
        self.password_eye_button.pack(side="right", padx=(theme.PADDING_SMALL, 0))
        self.show_password = False
        
        # Strength meter
        strength_frame = ctk.CTkFrame(password_frame, fg_color=theme.BG_PRIMARY)
        strength_frame.pack(fill="x", pady=(theme.PADDING_SMALL, 0))
        
        self.strength_bar = ctk.CTkProgressBar(
            strength_frame,
            width=300,
            height=6,
            corner_radius=3,
            fg_color=theme.BG_BORDER,
            progress_color=theme.DANGER_RED
        )
        self.strength_bar.pack(side="left", fill="x", expand=True)
        self.strength_bar.set(0)
        
        self.strength_label = ctk.CTkLabel(
            strength_frame,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.DANGER_RED
        )
        self.strength_label.pack(side="right", padx=(theme.PADDING_NORMAL, 0))
        
        # Notes field
        self._create_field(container, "Notes (optional)", "", multiline=True)
        self.notes_entry = self._last_entry
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        button_frame.pack(fill="x", pady=(theme.PADDING_XLARGE, 0))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="CANCEL",
            command=self.on_cancel,
            **theme.get_button_secondary_config(),
            width=150
        )
        cancel_button.pack(side="left", padx=(0, theme.PADDING_NORMAL))
        
        save_button = ctk.CTkButton(
            button_frame,
            text="SAVE",
            command=self._save_credential,
            **theme.get_button_primary_config(),
            width=150
        )
        save_button.pack(side="right")
    
    def _create_field(self, parent, label_text: str, placeholder: str, multiline: bool = False):
        """Helper to create a labeled input field."""
        frame = ctk.CTkFrame(parent, fg_color=theme.BG_PRIMARY)
        frame.pack(fill="x", pady=theme.PADDING_NORMAL)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        label.pack(anchor="w", pady=(0, theme.PADDING_SMALL))
        
        if multiline:
            entry = ctk.CTkTextbox(
                frame,
                fg_color=theme.BG_SECONDARY,
                border_color=theme.BG_BORDER,
                text_color=theme.TEXT_PRIMARY,
                font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
                height=80,
                corner_radius=theme.CORNER_RADIUS,
            )
        else:
            entry = ctk.CTkEntry(
                frame,
                placeholder_text=placeholder,
                **theme.get_input_config()
            )
        
        entry.pack(fill="x")
        self._last_entry = entry
    
    def _toggle_password_visibility(self):
        """Toggle password field visibility."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.password_eye_button.configure(text="👁‍🗨" if self.show_password else "👁")
    
    def _update_strength_meter(self, event=None):
        """Update strength meter based on password field."""
        password = self.password_entry.get()
        
        if not password:
            self.strength_bar.set(0)
            self.strength_label.configure(text="")
            return
        
        result = strength.evaluate_password_strength(password)
        score = result['score']
        
        self.strength_bar.set(score / 4)
        self.strength_bar.configure(progress_color=result['color'])
        self.strength_label.configure(text=result['label'], text_color=result['color'])
    
    def _open_generator(self):
        """Open password generator popup."""
        self.on_generate(self.password_entry, self._update_strength_meter)
    
    def _save_credential(self):
        """Save credential to database."""
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        notes = self.notes_entry.get("1.0", "end-1c").strip() if hasattr(self.notes_entry, 'get') and callable(getattr(self.notes_entry, 'get', None)) else ""
        
        # If notes_entry is a Textbox, get text differently
        if isinstance(self.notes_entry, ctk.CTkTextbox):
            notes = self.notes_entry.get("1.0", "end-1c").strip()
        else:
            notes = self.notes_entry.get().strip()
        
        # Validation
        if not website:
            self._show_error("Website/App name is required")
            return
        if not username:
            self._show_error("Username/Email is required")
            return
        if not password:
            self._show_error("Password is required")
            return
        
        # Encrypt password
        if not auth.session.aes_key:
            self._show_error("Session expired. Please log in again.")
            return
        
        ciphertext, iv, tag = crypto.encrypt_password(password, auth.session.aes_key)
        
        # Save to database
        try:
            if self.is_editing and self.credential_id:
                database.update_credential(
                    self.credential_id,
                    website, username, ciphertext, iv, tag, notes
                )
            else:
                credential_id = database.add_credential(
                    website, username, ciphertext, iv, tag, notes
                )
                self.credential_id = credential_id
            
            self.on_save(self.credential_id)
        except Exception as e:
            self._show_error(f"Error saving credential: {e}")
    
    def _show_error(self, message: str):
        """Show error message in a dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.configure(fg_color=theme.BG_PRIMARY)
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.DANGER_RED
        )
        label.pack(pady=theme.PADDING_XLARGE)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            **theme.get_button_primary_config(),
            width=100
        )
        ok_button.pack(pady=(0, theme.PADDING_NORMAL))
    
    def load_credential(self, credential_id: int):
        """Load existing credential for editing."""
        cred = database.get_credential(credential_id)
        if not cred or not auth.session.aes_key:
            return
        
        # Decrypt password
        password = crypto.decrypt_password(
            cred['encrypted_password'],
            cred['iv'],
            cred['tag'],
            auth.session.aes_key
        )
        
        self.credential_id = credential_id
        self.is_editing = True
        self.title_label.configure(text="Edit Credential")
        
        self.website_entry.delete(0, "end")
        self.website_entry.insert(0, cred['website'])
        
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, cred['username'])
        
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        
        self.notes_entry.delete("1.0", "end")
        self.notes_entry.insert("1.0", cred['notes'] or "")
        
        self._update_strength_meter()
    
    def reset_form(self):
        """Reset form for adding new credential."""
        self.credential_id = None
        self.is_editing = False
        self.title_label.configure(text="Add New Credential")
        
        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.notes_entry.delete("1.0", "end")
        
        self.strength_bar.set(0)
        self.strength_label.configure(text="")
        self.website_entry.focus()
