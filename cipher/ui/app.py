"""
Main application window for Cipher Password Manager.
Handles screen navigation, auto-lock on idle, and session management.
"""

import customtkinter as ctk
from typing import Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
import auth
from ui.login_screen import LoginScreen
from ui.setup_screen import SetupScreen
from ui.vault_screen import VaultScreen
from ui.add_edit_screen import AddEditScreen
from ui.generator_popup import GeneratorPopup
from ui import theme


class CipherApp(ctk.CTk):
    """Main application window."""
    
    IDLE_TIMEOUT = 300  # 5 minutes in seconds
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        self.title("Cipher")
        self.geometry(f"{theme.WINDOW_WIDTH}x{theme.WINDOW_HEIGHT}")
        self.minsize(theme.WINDOW_MIN_WIDTH, theme.WINDOW_MIN_HEIGHT)
        self.configure(fg_color=theme.BG_PRIMARY)
        
        # Initialize database
        database.ensure_db_exists()
        
        # Idle timer
        self._idle_timer = None
        self._current_screen = None
        self._screen_widgets = {}
        
        # Create screens
        self._create_screens()
        
        # Show appropriate startup screen
        self._show_startup_screen()
    
    def _create_screens(self):
        """Create all screen widgets."""
        # Login screen
        self._screen_widgets['login'] = LoginScreen(
            self,
            on_login_success=self._on_login_success,
            on_setup_needed=lambda: self._show_screen('setup')
        )
        self._screen_widgets['login'].pack(fill="both", expand=True)
        
        # Setup screen
        self._screen_widgets['setup'] = SetupScreen(
            self,
            on_setup_complete=lambda: self._show_screen('login')
        )
        self._screen_widgets['setup'].pack(fill="both", expand=True)
        
        # Vault screen
        self._screen_widgets['vault'] = VaultScreen(
            self,
            on_add_credential=self._on_add_credential,
            on_edit_credential=self._on_edit_credential,
            on_logout=self._on_logout
        )
        self._screen_widgets['vault'].pack(fill="both", expand=True)
        
        # Add/Edit screen
        self._screen_widgets['add_edit'] = AddEditScreen(
            self,
            on_save=self._on_credential_saved,
            on_cancel=lambda: self._show_screen('vault'),
            on_generate=self._open_generator
        )
        self._screen_widgets['add_edit'].pack(fill="both", expand=True)
    
    def _show_startup_screen(self):
        """Show appropriate startup screen (setup or login)."""
        if database.master_password_exists():
            self._show_screen('login')
        else:
            self._show_screen('setup')
    
    def _show_screen(self, screen_name: str):
        """
        Show a specific screen by name.
        
        Args:
            screen_name: One of 'login', 'setup', 'vault', 'add_edit'
        """
        # Hide all screens
        for name, screen in self._screen_widgets.items():
            screen.pack_forget()
        
        # Show selected screen
        if screen_name in self._screen_widgets:
            screen = self._screen_widgets[screen_name]
            screen.pack(fill="both", expand=True)
            
            # Notify screen it's being shown
            if hasattr(screen, 'on_show'):
                screen.on_show()
            
            self._current_screen = screen_name
            
            # Manage idle timer
            if screen_name == 'vault':
                # Start idle timer when in vault
                self._reset_idle_timer()
                self._bind_activity_events()
            else:
                # Stop idle timer when not in vault
                self._cancel_idle_timer()
                self._unbind_activity_events()
    
    def _on_login_success(self):
        """Called when user successfully logs in."""
        self._show_screen('vault')
    
    def _on_add_credential(self):
        """Show add new credential form."""
        self._screen_widgets['add_edit'].reset_form()
        self._show_screen('add_edit')
    
    def _on_edit_credential(self, credential_id: int):
        """Show edit credential form."""
        self._screen_widgets['add_edit'].load_credential(credential_id)
        self._show_screen('add_edit')
    
    def _on_credential_saved(self, credential_id: int):
        """Called when credential is saved."""
        self._show_screen('vault')
    
    def _on_logout(self):
        """Handle logout button."""
        self._lock_vault()
    
    def _lock_vault(self, show_inactivity_message: bool = False):
        """Lock vault and return to login screen."""
        # Clear session
        auth.lock_session()
        
        # Cancel idle timer
        self._cancel_idle_timer()
        self._unbind_activity_events()
        
        # Show login screen
        if show_inactivity_message:
            self._show_screen('login')
            self._screen_widgets['login'].show_inactivity_message()
        else:
            self._show_screen('login')
    
    # ========================================================================
    # IDLE TIMEOUT & ACTIVITY MANAGEMENT
    # ========================================================================
    
    def _reset_idle_timer(self):
        """Reset idle timer."""
        if self._idle_timer:
            self.after_cancel(self._idle_timer)
        
        self._idle_timer = self.after(self.IDLE_TIMEOUT * 1000, self._on_idle_timeout)
    
    def _cancel_idle_timer(self):
        """Cancel idle timer."""
        if self._idle_timer:
            self.after_cancel(self._idle_timer)
            self._idle_timer = None
    
    def _on_idle_timeout(self):
        """Called when idle timeout expires."""
        self._lock_vault(show_inactivity_message=True)
    
    def _bind_activity_events(self):
        """Bind activity events to reset idle timer."""
        # Bind various events to reset the idle timer
        self.bind_all('<Motion>', self._on_activity)
        self.bind_all('<KeyPress>', self._on_activity)
        self.bind_all('<Button>', self._on_activity)
    
    def _unbind_activity_events(self):
        """Unbind activity events."""
        self.unbind_all('<Motion>')
        self.unbind_all('<KeyPress>')
        self.unbind_all('<Button>')
    
    def _on_activity(self, event=None):
        """Handle user activity."""
        if self._current_screen == 'vault':
            self._reset_idle_timer()
    
    # ========================================================================
    # PASSWORD GENERATOR POPUP
    # ========================================================================
    
    def _open_generator(self, password_entry, on_updated_callback):
        """Open password generator popup."""
        GeneratorPopup(self, password_entry, on_updated_callback)


def main():
    """Entry point for the application."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = CipherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
