"""
utils/helpers.py
----------------
Utility functions for parsing, formatting, and validating inputs.
"""

import re


def sanitize_product_name(name: str) -> str:
    """Clean up product name input."""
    return name.strip().title()


def parse_vs_input(user_input: str):
    """
    Parse a 'Product A vs Product B' style input.
    Returns (product_a, product_b) or (None, None) if format is invalid.
    """
    separators = [" vs ", " VS ", " Vs ", " versus ", " or "]
    for sep in separators:
        if sep in user_input:
            parts = user_input.split(sep, 1)
            return sanitize_product_name(parts[0]), sanitize_product_name(parts[1])
    return None, None


def extract_recommendation(comparison_text: str) -> str:
    """
    Extract just the recommendation section from a full comparison report.
    """
    lines = comparison_text.split("\n")
    rec_start = None
    for i, line in enumerate(lines):
        if "Recommendation" in line or "🏆" in line:
            rec_start = i
            break

    if rec_start is not None:
        return "\n".join(lines[rec_start:]).strip()
    return comparison_text


def format_product_label(name: str) -> str:
    """Format a product name for display."""
    return f"🔷 {name}"


def truncate_text(text: str, max_chars: int = 300) -> str:
    """Truncate long text with ellipsis."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."
