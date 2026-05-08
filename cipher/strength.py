"""
Password strength evaluation for Cipher Password Manager.
Uses the zxcvbn library for real-world strength scoring.
"""

from zxcvbn import zxcvbn
from typing import Dict, Tuple


# Color mapping for strength scores
STRENGTH_COLORS = {
    0: "#E53935",  # Red - Very Weak
    1: "#FF7043",  # Orange - Weak
    2: "#FFB300",  # Yellow/Gold - Fair
    3: "#7CB342",  # Light Green - Strong
    4: "#00897B",  # Teal - Very Strong
}

# Label mapping for strength scores
STRENGTH_LABELS = {
    0: "Very Weak",
    1: "Weak",
    2: "Fair",
    3: "Strong",
    4: "Very Strong",
}


def evaluate_password_strength(password: str) -> Dict:
    """
    Evaluate password strength using zxcvbn algorithm.
    
    Args:
        password: Password string to evaluate
        
    Returns:
        Dict with keys:
            - 'score': 0-4 integer (0=Very Weak, 4=Very Strong)
            - 'label': Human-readable strength label
            - 'color': Hex color code for UI display
            - 'feedback': Dict with suggestions (from zxcvbn)
            - 'entropy': Estimated entropy bits
    """
    if not password:
        return {
            'score': 0,
            'label': 'Very Weak',
            'color': STRENGTH_COLORS[0],
            'feedback': {},
            'entropy': 0
        }
    
    result = zxcvbn(password)
    
    return {
        'score': result['score'],
        'label': STRENGTH_LABELS[result['score']],
        'color': STRENGTH_COLORS[result['score']],
        'feedback': result.get('feedback', {}),
        'entropy': result.get('guesses_log10', 0)
    }


def get_strength_color(score: int) -> str:
    """Get hex color for a strength score (0-4)."""
    return STRENGTH_COLORS.get(score, STRENGTH_COLORS[0])


def get_strength_label(score: int) -> str:
    """Get text label for a strength score (0-4)."""
    return STRENGTH_LABELS.get(score, STRENGTH_LABELS[0])
