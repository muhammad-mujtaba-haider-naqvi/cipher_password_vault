"""
Vault screen for Cipher Password Manager.
Displays all stored credentials with search, copy, edit, and delete functionality.
"""

import customtkinter as ctk
from typing import Callable, List, Dict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
import auth
import crypto
import clipboard_manager
from cryptography.exceptions import InvalidTag
from ui import theme


class VaultScreen(ctk.CTkFrame):
    """Main vault display with credential list and search."""
    
    def __init__(self, parent, on_add_credential: Callable, on_edit_credential: Callable,
                 on_logout: Callable, **kwargs):
        """
        Initialize vault screen.
        
        Args:
            parent: Parent widget
            on_add_credential: Callback when "Add" button clicked () -> None
            on_edit_credential: Callback when edit button clicked (credential_id) -> None
            on_logout: Callback when logout button clicked () -> None
        """
        super().__init__(parent, **theme.get_main_frame_config(), **kwargs)
        
        self.on_add_credential = on_add_credential
        self.on_edit_credential = on_edit_credential
        self.on_logout = on_logout
        
        self.credentials: List[Dict] = []
        self.copy_timers = {}  # Track countdown timers for each entry
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout UI elements."""
        # Header frame
        header = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY)
        header.pack(fill="x", padx=theme.PADDING_XLARGE, pady=(theme.PADDING_XLARGE, theme.PADDING_NORMAL))
        
        # Left side - title
        left_frame = ctk.CTkFrame(header, fg_color=theme.BG_PRIMARY)
        left_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            left_frame,
            text="🔐 CIPHER",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_XLARGE, "bold"),
            text_color=theme.ACCENT_PRIMARY
        )
        title.pack(side="left", padx=(0, theme.PADDING_XLARGE))
        
        # Center - Search bar
        search_frame = ctk.CTkFrame(header, fg_color=theme.BG_PRIMARY)
        search_frame.pack(side="left", fill="x", expand=True, padx=theme.PADDING_NORMAL)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=(theme.FONT_FAMILY, 14),
            text_color=theme.TEXT_SECONDARY
        )
        search_label.pack(side="left", padx=(0, theme.PADDING_SMALL))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search websites, usernames...",
            **theme.get_input_config()
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)
        
        # Right side - Buttons
        button_frame = ctk.CTkFrame(header, fg_color=theme.BG_PRIMARY)
        button_frame.pack(side="right", padx=(theme.PADDING_NORMAL, 0))
        
        add_button = ctk.CTkButton(
            button_frame,
            text="+ ADD",
            command=self.on_add_credential,
            **theme.get_button_primary_config(),
            width=80
        )
        add_button.pack(side="left", padx=(0, theme.PADDING_SMALL))
        
        logout_button = ctk.CTkButton(
            button_frame,
            text="🔒",
            command=self.on_logout,
            width=44,
            **theme.get_button_secondary_config()
        )
        logout_button.pack(side="left")
        
        # Separator
        separator = ctk.CTkFrame(self, height=1, fg_color=theme.BG_BORDER)
        separator.pack(fill="x")
        
        # Vault list (scrollable)
        list_container = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY)
        list_container.pack(fill="both", expand=True, padx=theme.PADDING_XLARGE,
                           pady=theme.PADDING_XLARGE)
        
        # Scrollable frame for credentials
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color=theme.BG_PRIMARY,
            label_text="Stored Credentials"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="No credentials stored yet. Click '+ ADD' to add your first entry.",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_SECONDARY
        )
        
        # Footer
        self.footer_label = ctk.CTkLabel(
            self,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.TEXT_SECONDARY
        )
        self.footer_label.pack(pady=(0, theme.PADDING_NORMAL), padx=theme.PADDING_XLARGE)
    
    def _on_search_changed(self, event=None):
        """Handle search input changes."""
        query = self.search_entry.get().strip()
        if query:
            self.credentials = database.search_credentials(query)
        else:
            self.credentials = database.get_all_credentials()
        
        self._render_credentials()
    
    def _render_credentials(self):
        """Render credential list based on current data."""
        # Cancel all pending countdown timers before destroying widgets
        for timer_id in list(self.copy_timers.values()):
            try:
                self.after_cancel(timer_id)
            except:
                pass
        self.copy_timers.clear()
        
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.credentials:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No credentials stored yet. Click '+ ADD' to add your first entry.",
                font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
                text_color=theme.TEXT_SECONDARY
            )
            empty_label.pack(pady=theme.PADDING_XLARGE)
            self.footer_label.configure(text="0 entries stored")
            return
        
        # Render each credential
        for cred in self.credentials:
            self._create_credential_card(cred)
        
        # Update footer
        count = len(self.credentials)
        self.footer_label.configure(text=f"{count} {'entry' if count == 1 else 'entries'} stored")
    
    def _create_credential_card(self, credential: Dict):
        """Create a UI card for a single credential."""
        card = ctk.CTkFrame(
            self.scrollable_frame,
            **theme.get_frame_config(),
            height=80
        )
        card.pack(fill="x", pady=theme.PADDING_NORMAL)
        card.pack_propagate(False)
        
        # Left side - credential info
        info_frame = ctk.CTkFrame(card, fg_color=theme.BG_SECONDARY)
        info_frame.pack(side="left", fill="both", expand=True, padx=theme.PADDING_NORMAL,
                       pady=theme.PADDING_NORMAL)
        
        website_label = ctk.CTkLabel(
            info_frame,
            text=f"🌐  {credential['website']}",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_LARGE, "bold"),
            text_color=theme.TEXT_PRIMARY
        )
        website_label.pack(anchor="w")
        
        username_label = ctk.CTkLabel(
            info_frame,
            text=credential['username'],
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_SECONDARY
        )
        username_label.pack(anchor="w")
        
        # Right side - action buttons
        button_frame = ctk.CTkFrame(card, fg_color=theme.BG_SECONDARY)
        button_frame.pack(side="right", padx=theme.PADDING_NORMAL, pady=theme.PADDING_NORMAL)
        
        # Copy button with countdown
        copy_button_frame = ctk.CTkFrame(button_frame, fg_color=theme.BG_SECONDARY)
        copy_button_frame.pack(side="left", padx=(0, theme.PADDING_SMALL))
        
        copy_button = ctk.CTkButton(
            copy_button_frame,
            text="📋 Copy",
            command=lambda: self._copy_password(credential['id'], copy_button, countdown_label),
            **theme.get_button_secondary_config(),
            width=90
        )
        copy_button.pack(side="left")
        
        countdown_label = ctk.CTkLabel(
            copy_button_frame,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.TEXT_SECONDARY
        )
        countdown_label.pack(side="left", padx=(theme.PADDING_SMALL, 0))
        
        # Edit button
        edit_button = ctk.CTkButton(
            button_frame,
            text="✏",
            command=lambda: self.on_edit_credential(credential['id']),
            width=32,
            **theme.get_button_secondary_config()
        )
        edit_button.pack(side="left", padx=(0, theme.PADDING_SMALL))
        
        # Delete button
        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑",
            command=lambda: self._delete_credential(credential['id']),
            width=32,
            **theme.get_button_secondary_config()
        )
        delete_button.pack(side="left")
    
    def _copy_password(self, credential_id: int, copy_button, countdown_label):
        """Copy password to clipboard and show countdown."""
        try:
            # Get credential and decrypt password
            cred = database.get_credential(credential_id)
            if not cred or not auth.session.aes_key:
                return
            
            password = crypto.decrypt_password(
                cred['encrypted_password'],
                cred['iv'],
                cred['tag'],
                auth.session.aes_key
            )
            
            # Cancel any existing timer for this entry
            if credential_id in self.copy_timers:
                self.after_cancel(self.copy_timers[credential_id])
            
            # Copy to clipboard with auto-clear
            def on_cleared():
                try:
                    if copy_button.winfo_exists():
                        copy_button.configure(text="📋 Copy", text_color=theme.TEXT_SECONDARY)
                    if countdown_label.winfo_exists():
                        countdown_label.configure(text="")
                except:
                    pass
            
            clipboard_manager.copy_with_auto_clear(password, 30, on_cleared)
            
            # Update UI
            copy_button.configure(text="✓ Copied", text_color=theme.SUCCESS_GREEN)
            
            # Start countdown
            def countdown(remaining=30):
                if remaining > 0:
                    # Check if label widget still exists before updating
                    try:
                        if countdown_label.winfo_exists():
                            countdown_label.configure(text=f"Clears in {remaining}s")
                            self.copy_timers[credential_id] = self.after(
                                1000,
                                lambda: countdown(remaining - 1)
                            )
                    except:
                        pass
                else:
                    try:
                        if countdown_label.winfo_exists():
                            countdown_label.configure(text="")
                    except:
                        pass
            
            countdown()
            
        except InvalidTag:
            self._show_error_dialog(
                "Unable to decrypt this password.\n"
                "It may have been encrypted with a different master password."
            )
        except Exception:
            self._show_error_dialog("Unable to copy password right now. Please try again.")
    
    def _show_error_dialog(self, message: str):
        """Show an error dialog in the vault screen."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("360x130")
        dialog.resizable(False, False)
        dialog.configure(fg_color=theme.BG_PRIMARY)
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        dialog.focus()

        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.DANGER_RED,
            justify="center"
        )
        label.pack(pady=theme.PADDING_XLARGE)

        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            **theme.get_button_primary_config(),
            width=100
        )
        ok_btn.pack(pady=(0, theme.PADDING_NORMAL))

    def _delete_credential(self, credential_id: int):
        """Delete a credential after confirmation."""
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Delete Credential")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.configure(fg_color=theme.BG_PRIMARY)
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        dialog.focus()
        
        msg = ctk.CTkLabel(
            dialog,
            text="Delete this credential?\nThis cannot be undone.",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        msg.pack(pady=theme.PADDING_XLARGE)
        
        button_frame = ctk.CTkFrame(dialog, fg_color=theme.BG_PRIMARY)
        button_frame.pack(pady=(0, theme.PADDING_NORMAL))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            **theme.get_button_secondary_config(),
            width=100
        )
        cancel_btn.pack(side="left", padx=theme.PADDING_SMALL)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=lambda: [database.delete_credential(credential_id), dialog.destroy(), self.refresh()],
            **theme.get_button_danger_config(),
            width=100
        )
        delete_btn.pack(side="left", padx=theme.PADDING_SMALL)
    
    def on_show(self):
        """Called when screen is shown."""
        self.refresh()
    
    def refresh(self):
        """Refresh credential list from database."""
        self.credentials = database.get_all_credentials()
        self._render_credentials()
