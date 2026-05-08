"""
Theme configuration for Cipher Password Manager.
Centralized colors, fonts, and styling constants for the entire application.
"""

# ============================================================================
# COLOR SCHEME - Dark Vault Aesthetic
# ============================================================================

# Background colors
BG_PRIMARY = "#0F0F0F"      # Main background
BG_SECONDARY = "#1A1A1A"    # Card/frame background
BG_TERTIARY = "#252525"     # Hover states
BG_BORDER = "#2A2A2A"       # Border color

# Accent colors
ACCENT_PRIMARY = "#00BFA5"  # Primary action, highlights
ACCENT_DARK = "#00897B"     # Darker accent for hover
ACCENT_LIGHT = "#26C6DA"    # Lighter accent for variants

# Semantic colors
DANGER_RED = "#E53935"      # Errors, lockout, delete
WARNING_ORANGE = "#FF7043"  # Warnings
SUCCESS_GREEN = "#7CB342"   # Success, strong password

# Text colors
TEXT_PRIMARY = "#FFFFFF"    # Main text
TEXT_SECONDARY = "#9E9E9E"  # Secondary text, muted
TEXT_MUTED = "#555555"      # Placeholder, disabled
TEXT_DARK = "#000000"       # For light backgrounds (buttons)

# ============================================================================
# FONTS
# ============================================================================

# Font family - platform dependent fallback
FONT_FAMILY = "Segoe UI"    # Primary
FONT_FAMILY_MONO = "Courier New"

# Font sizes
FONT_SIZE_SMALL = 11        # Small text, buttons
FONT_SIZE_NORMAL = 13       # Default text, input
FONT_SIZE_LARGE = 14        # Labels, medium emphasis
FONT_SIZE_XLARGE = 16       # Titles, headers
FONT_SIZE_TITLE = 20        # Main titles, large headers

# ============================================================================
# DIMENSIONS
# ============================================================================

CORNER_RADIUS = 8           # Standard border radius
CORNER_RADIUS_LARGE = 10    # Larger elements

PADDING_SMALL = 5
PADDING_NORMAL = 10
PADDING_LARGE = 15
PADDING_XLARGE = 20

INPUT_HEIGHT = 44           # Standard input field height
BUTTON_HEIGHT = 44          # Standard button height
ICON_SIZE = 20              # Icon dimensions

# ============================================================================
# WINDOW DIMENSIONS
# ============================================================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 620
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 560

# ============================================================================
# BUTTON STYLES (CustomTkinter CTkButton configs)
# ============================================================================

def get_button_primary_config():
    """Returns config dict for primary action buttons (teal)."""
    return {
        'fg_color': ACCENT_PRIMARY,
        'hover_color': ACCENT_DARK,
        'text_color': TEXT_DARK,
        'font': (FONT_FAMILY, FONT_SIZE_LARGE, 'bold'),
        'corner_radius': CORNER_RADIUS,
        'height': BUTTON_HEIGHT
    }


def get_button_secondary_config():
    """Returns config dict for secondary buttons (transparent with border)."""
    return {
        'fg_color': 'transparent',
        'border_color': BG_BORDER,
        'border_width': 1,
        'hover_color': BG_TERTIARY,
        'text_color': TEXT_SECONDARY,
        'font': (FONT_FAMILY, FONT_SIZE_NORMAL),
        'corner_radius': CORNER_RADIUS,
        'height': BUTTON_HEIGHT,
    }


def get_button_danger_config():
    """Returns config dict for danger buttons (red)."""
    return {
        'fg_color': DANGER_RED,
        'hover_color': '#C62828',
        'text_color': TEXT_PRIMARY,
        'font': (FONT_FAMILY, FONT_SIZE_NORMAL, 'bold'),
        'corner_radius': CORNER_RADIUS,
    }


# ============================================================================
# INPUT STYLES
# ============================================================================

def get_input_config():
    """Returns config dict for CTkEntry fields."""
    return {
        'fg_color': BG_SECONDARY,
        'border_color': BG_BORDER,
        'text_color': TEXT_PRIMARY,
        'placeholder_text_color': TEXT_MUTED,
        'font': (FONT_FAMILY, FONT_SIZE_NORMAL),
        'height': INPUT_HEIGHT,
        'corner_radius': CORNER_RADIUS,
    }


# ============================================================================
# FRAME STYLES
# ============================================================================

def get_frame_config():
    """Returns config dict for CTkFrame (card-like elements)."""
    return {
        'fg_color': BG_SECONDARY,
        'border_color': BG_BORDER,
        'border_width': 1,
        'corner_radius': CORNER_RADIUS_LARGE
    }


def get_main_frame_config():
    """Returns config dict for main content frames."""
    return {
        'fg_color': BG_PRIMARY,
    }
