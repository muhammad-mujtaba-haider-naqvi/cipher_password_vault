"""
Password generator popup for Cipher Password Manager.
Modal window for generating passwords with customizable options.
"""

import customtkinter as ctk
from typing import Callable

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generator
import strength
from ui import theme


class GeneratorPopup(ctk.CTkToplevel):
    """Modal popup for password generation."""
    
    def __init__(self, parent, password_entry: ctk.CTkEntry, on_updated: Callable = None):
        """
        Initialize generator popup.
        
        Args:
            parent: Parent window
            password_entry: CTkEntry widget to insert password into
            on_updated: Optional callback when password is updated
        """
        super().__init__(parent)
        
        self.password_entry = password_entry
        self.on_updated = on_updated
        self.generated_password = ""
        
        self.title("Password Generator")
        self.geometry("480x700")
        self.resizable(False, False)
        self.configure(fg_color=theme.BG_PRIMARY)
        
        # Focus on this window
        self.grab_set()
        self.focus()
        
        self._create_widgets()
        self._generate_password()
    
    def _create_widgets(self):
        """Create popup UI."""
        container = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY)
        container.pack(fill="both", expand=True, padx=theme.PADDING_XLARGE,
                      pady=theme.PADDING_XLARGE)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="⚡ Generate Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_XLARGE, "bold"),
            text_color=theme.ACCENT_PRIMARY
        )
        title.pack(anchor="w", pady=(0, theme.PADDING_XLARGE))
        
        # Length slider
        length_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        length_frame.pack(fill="x", pady=theme.PADDING_NORMAL)
        
        length_label = ctk.CTkLabel(
            length_frame,
            text="Length: ",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        length_label.pack(side="left")
        
        self.length_value_label = ctk.CTkLabel(
            length_frame,
            text="16",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL, "bold"),
            text_color=theme.ACCENT_PRIMARY
        )
        self.length_value_label.pack(side="left", padx=(0, theme.PADDING_NORMAL))
        
        self.length_slider = ctk.CTkSlider(
            container,
            from_=8,
            to=64,
            number_of_steps=56,
            button_color=theme.ACCENT_PRIMARY,
            progress_color=theme.ACCENT_PRIMARY,
            fg_color=theme.BG_BORDER,
            command=self._on_length_changed
        )
        self.length_slider.pack(fill="x", pady=theme.PADDING_NORMAL)
        self.length_slider.set(16)
        
        # Character type checkboxes
        chars_label = ctk.CTkLabel(
            container,
            text="Character Types",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL, "bold"),
            text_color=theme.TEXT_PRIMARY
        )
        chars_label.pack(anchor="w", pady=(theme.PADDING_XLARGE, theme.PADDING_NORMAL))
        
        self.upper_check = ctk.CTkCheckBox(
            container,
            text="Uppercase (A-Z)",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY,
            checkmark_color=theme.ACCENT_PRIMARY,
            command=self._generate_password
        )
        self.upper_check.pack(anchor="w", pady=theme.PADDING_SMALL)
        self.upper_check.select()
        
        self.lower_check = ctk.CTkCheckBox(
            container,
            text="Lowercase (a-z)",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY,
            checkmark_color=theme.ACCENT_PRIMARY,
            command=self._generate_password
        )
        self.lower_check.pack(anchor="w", pady=theme.PADDING_SMALL)
        self.lower_check.select()
        
        self.digits_check = ctk.CTkCheckBox(
            container,
            text="Digits (0-9)",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY,
            checkmark_color=theme.ACCENT_PRIMARY,
            command=self._generate_password
        )
        self.digits_check.pack(anchor="w", pady=theme.PADDING_SMALL)
        self.digits_check.select()
        
        self.symbols_check = ctk.CTkCheckBox(
            container,
            text="Symbols (!@#$%...)",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY,
            checkmark_color=theme.ACCENT_PRIMARY,
            command=self._generate_password
        )
        self.symbols_check.pack(anchor="w", pady=theme.PADDING_SMALL)
        self.symbols_check.select()
        
        # Generated password display
        display_label = ctk.CTkLabel(
            container,
            text="Generated Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL, "bold"),
            text_color=theme.TEXT_PRIMARY
        )
        display_label.pack(anchor="w", pady=(theme.PADDING_XLARGE, theme.PADDING_SMALL))
        
        self.password_display = ctk.CTkEntry(
            container,
            **theme.get_input_config()
        )
        self.password_display.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        self.password_display.configure(state="readonly")

        use_now_button = ctk.CTkButton(
            container,
            text="Use Password in Form",
            command=self._use_password,
            **theme.get_button_primary_config()
        )
        use_now_button.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        
        # Strength meter for generated password
        strength_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        strength_frame.pack(fill="x", pady=(theme.PADDING_SMALL, theme.PADDING_NORMAL))
        
        self.strength_bar = ctk.CTkProgressBar(
            strength_frame,
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
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        button_frame.pack(fill="x", pady=(theme.PADDING_NORMAL, 0))
        
        regen_button = ctk.CTkButton(
            button_frame,
            text="🔄 Regenerate",
            command=self._generate_password,
            **theme.get_button_secondary_config()
        )
        regen_button.pack(side="left", padx=(0, theme.PADDING_NORMAL), fill="x", expand=True)
        
        use_button = ctk.CTkButton(
            button_frame,
            text="✓ Copy & Use",
            command=self._use_password,
            **theme.get_button_primary_config()
        )
        use_button.pack(side="right", fill="x", expand=True)
    
    def _on_length_changed(self, value):
        """Update length slider display."""
        length = int(value)
        self.length_value_label.configure(text=str(length))
        self._generate_password()
    
    def _generate_password(self):
        """Generate a new password based on settings."""
        length = int(self.length_slider.get())
        use_upper = self.upper_check.get()
        use_lower = self.lower_check.get()
        use_digits = self.digits_check.get()
        use_symbols = self.symbols_check.get()
        
        # Validate at least one type selected
        if not any([use_upper, use_lower, use_digits, use_symbols]):
            self.upper_check.select()
            use_upper = True
        
        try:
            self.generated_password = generator.generate_password(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols
            )
        except ValueError as e:
            self.generated_password = ""
            return
        
        # Update display
        self.password_display.configure(state="normal")
        self.password_display.delete(0, "end")
        self.password_display.insert(0, self.generated_password)
        self.password_display.configure(state="readonly")
        
        # Update strength meter
        result = strength.evaluate_password_strength(self.generated_password)
        score = result['score']
        self.strength_bar.set(score / 4)
        self.strength_bar.configure(progress_color=result['color'])
        self.strength_label.configure(text=result['label'], text_color=result['color'])
    
    def _use_password(self):
        """Use the generated password and close popup."""
        if self.generated_password:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, self.generated_password)
            
            if self.on_updated:
                self.on_updated()
            
            self.destroy()
