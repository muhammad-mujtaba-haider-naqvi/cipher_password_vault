"""
Setup screen for Cipher Password Manager.
Allows user to create master password on first use.
"""

import customtkinter as ctk
from typing import Callable

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import strength
import master_auth
from ui import theme


class SetupScreen(ctk.CTkFrame):
    """Initial master password setup screen."""
    
    def __init__(self, parent, on_setup_complete: Callable, **kwargs):
        """
        Initialize setup screen.
        
        Args:
            parent: Parent widget
            on_setup_complete: Callback when setup completes () -> None
        """
        super().__init__(parent, **theme.get_main_frame_config(), **kwargs)
        
        self.on_setup_complete = on_setup_complete
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout UI elements."""
        container = ctk.CTkScrollableFrame(self, fg_color=theme.BG_PRIMARY)
        container.pack(fill="both", expand=True, padx=theme.PADDING_XLARGE,
                      pady=theme.PADDING_XLARGE)
        
        # Title
        title_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        title_frame.pack(pady=(0, theme.PADDING_XLARGE))
        
        title = ctk.CTkLabel(
            title_frame,
            text="🔐 Set Master Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_TITLE, "bold"),
            text_color=theme.ACCENT_PRIMARY
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Create a strong password to secure your vault",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_SECONDARY
        )
        subtitle.pack(pady=(theme.PADDING_NORMAL, 0))
        
        # Warning
        warning = ctk.CTkLabel(
            container,
            text="⚠️  Set up recovery to reset your master password securely.",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.WARNING_ORANGE,
            wraplength=400
        )
        warning.pack(pady=(0, theme.PADDING_XLARGE))
        
        # Password field
        label1 = ctk.CTkLabel(
            container,
            text="Master Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        label1.pack(anchor="w", pady=(0, theme.PADDING_SMALL))
        
        password_container = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        password_container.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="Enter master password",
            show="*",
            **theme.get_input_config()
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.bind("<KeyRelease>", self._update_strength)
        
        # Eye button
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
            command=self._toggle_visibility,
            corner_radius=theme.CORNER_RADIUS
        )
        self.eye_button.pack(side="right", padx=(theme.PADDING_SMALL, 0))
        self.show_password = False
        
        # Strength meter
        strength_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        strength_frame.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        
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
        
        # Confirm password field
        label2 = ctk.CTkLabel(
            container,
            text="Confirm Master Password",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        label2.pack(anchor="w", pady=(theme.PADDING_XLARGE, theme.PADDING_SMALL))
        
        confirm_container = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        confirm_container.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        
        self.confirm_entry = ctk.CTkEntry(
            confirm_container,
            placeholder_text="Re-enter master password",
            show="*",
            **theme.get_input_config()
        )
        self.confirm_entry.pack(side="left", fill="x", expand=True)
        self.confirm_entry.bind("<Return>", lambda e: self._setup_master_password())
        
        # Confirm eye button
        self.confirm_eye_button = ctk.CTkButton(
            confirm_container,
            text="👁",
            width=45,
            height=theme.INPUT_HEIGHT,
            fg_color=theme.BG_SECONDARY,
            hover_color=theme.BG_TERTIARY,
            border_color=theme.BG_BORDER,
            border_width=1,
            font=(theme.FONT_FAMILY, 16),
            command=self._toggle_confirm_visibility,
            corner_radius=theme.CORNER_RADIUS
        )
        self.confirm_eye_button.pack(side="right", padx=(theme.PADDING_SMALL, 0))
        self.show_confirm = False

        # Recovery question
        recovery_label = ctk.CTkLabel(
            container,
            text="Recovery Security Question",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        recovery_label.pack(anchor="w", pady=(theme.PADDING_XLARGE, theme.PADDING_SMALL))

        self.recovery_question_var = ctk.StringVar(value=master_auth.RECOVERY_QUESTIONS[0])
        self.recovery_question_menu = ctk.CTkOptionMenu(
            container,
            values=master_auth.RECOVERY_QUESTIONS,
            variable=self.recovery_question_var,
            fg_color=theme.BG_SECONDARY,
            button_color=theme.ACCENT_PRIMARY,
            button_hover_color=theme.ACCENT_DARK,
            text_color=theme.TEXT_PRIMARY,
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            command=self._on_recovery_question_changed,
            height=theme.INPUT_HEIGHT
        )
        self.recovery_question_menu.pack(fill="x", pady=(0, theme.PADDING_NORMAL))

        self.custom_question_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter custom recovery question",
            **theme.get_input_config()
        )

        recovery_answer_label = ctk.CTkLabel(
            container,
            text="Recovery Answer",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_NORMAL),
            text_color=theme.TEXT_PRIMARY
        )
        recovery_answer_label.pack(anchor="w", pady=(0, theme.PADDING_SMALL))

        self.recovery_answer_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter recovery answer",
            **theme.get_input_config()
        )
        self.recovery_answer_entry.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        
        # Error message
        self.error_label = ctk.CTkLabel(
            container,
            text="",
            font=(theme.FONT_FAMILY, theme.FONT_SIZE_SMALL),
            text_color=theme.DANGER_RED
        )
        self.error_label.pack(pady=(theme.PADDING_NORMAL, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color=theme.BG_PRIMARY)
        button_frame.pack(fill="x", pady=(theme.PADDING_XLARGE, 0))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="CANCEL",
            command=self.on_setup_complete,  # Goes back to login
            **theme.get_button_secondary_config(),
            width=150
        )
        cancel_button.pack(side="left", padx=(0, theme.PADDING_NORMAL))
        
        self.create_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=self._setup_master_password,
            **theme.get_button_primary_config(),
            width=150
        )
        self.create_button.pack(side="right")

    def _on_recovery_question_changed(self, selected_value: str):
        """Show custom question field only when selected."""
        if selected_value == "Custom question":
            self.custom_question_entry.pack(fill="x", pady=(0, theme.PADDING_NORMAL))
        else:
            self.custom_question_entry.pack_forget()
    
    def _toggle_visibility(self):
        """Toggle master password visibility."""
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.eye_button.configure(text="👁‍🗨" if self.show_password else "👁")
    
    def _toggle_confirm_visibility(self):
        """Toggle confirm password visibility."""
        self.show_confirm = not self.show_confirm
        self.confirm_entry.configure(show="" if self.show_confirm else "*")
        self.confirm_eye_button.configure(text="👁‍🗨" if self.show_confirm else "👁")
    
    def _update_strength(self, event=None):
        """Update strength meter."""
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
    
    def _setup_master_password(self):
        """Create master password."""
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        question = self.recovery_question_var.get()
        if question == "Custom question":
            question = self.custom_question_entry.get().strip()
        answer = self.recovery_answer_entry.get().strip()
        
        # Validation
        if not password:
            self.error_label.configure(text="Please enter a master password")
            return
        
        if len(password) < 8:
            self.error_label.configure(text="Password must be at least 8 characters")
            return
        
        if password != confirm:
            self.error_label.configure(text="Passwords do not match")
            self.confirm_entry.delete(0, "end")
            self.confirm_entry.focus()
            return

        if not question:
            self.error_label.configure(text="Please select or enter a recovery question")
            return

        if not answer:
            self.error_label.configure(text="Please enter recovery answer")
            return
        
        success, message = master_auth.setup_master_password(password, question, answer)
        if not success:
            self.error_label.configure(text=message)
            return
        
        self.error_label.configure(text="")
        self.on_setup_complete()
    
    def on_show(self):
        """Called when screen is shown."""
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")
        self.recovery_question_var.set(master_auth.RECOVERY_QUESTIONS[0])
        self.custom_question_entry.delete(0, "end")
        self.custom_question_entry.pack_forget()
        self.recovery_answer_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.strength_bar.set(0)
        self.strength_label.configure(text="")
        self.password_entry.focus()
