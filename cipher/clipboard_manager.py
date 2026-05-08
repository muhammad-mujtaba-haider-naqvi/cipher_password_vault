"""
Clipboard management for Cipher Password Manager.
Handles copy to clipboard with automatic clearing after delay.
"""

import pyperclip
import threading
from typing import Optional, Callable


_clear_timer: Optional[threading.Timer] = None


def copy_with_auto_clear(
    text: str,
    delay_seconds: int = 30,
    on_cleared_callback: Optional[Callable] = None
) -> None:
    """
    Copy text to clipboard and schedule automatic clearing after delay.
    
    Only one auto-clear can be active at a time. Calling this function
    while another operation is pending will cancel the previous timer.
    
    Args:
        text: Text to copy to clipboard
        delay_seconds: Seconds before clipboard is cleared (default 30)
        on_cleared_callback: Optional callback function to call when clipboard is cleared
    """
    global _clear_timer
    
    # Cancel previous timer if any
    if _clear_timer is not None:
        _clear_timer.cancel()
    
    # Copy to clipboard
    try:
        pyperclip.copy(text)
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return
    
    def clear_clipboard():
        """Clear clipboard if it still contains the original text."""
        try:
            if pyperclip.paste() == text:
                pyperclip.copy("")
        except Exception:
            pass
        
        if on_cleared_callback:
            try:
                on_cleared_callback()
            except Exception as e:
                print(f"Error in cleared callback: {e}")
    
    # Schedule clearing
    _clear_timer = threading.Timer(delay_seconds, clear_clipboard)
    _clear_timer.daemon = True
    _clear_timer.start()


def cancel_auto_clear() -> None:
    """Cancel any pending auto-clear operation."""
    global _clear_timer
    if _clear_timer:
        _clear_timer.cancel()
        _clear_timer = None
