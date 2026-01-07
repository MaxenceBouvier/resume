"""Utility functions for resume builder."""

import re

# LaTeX special characters that need escaping
LATEX_SPECIAL_CHARS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# Pre-compiled regex pattern for efficiency
_LATEX_ESCAPE_PATTERN = re.compile("|".join(re.escape(k) for k in LATEX_SPECIAL_CHARS))


def escape_latex(text: str) -> str:
    """
    Escape special characters for LaTeX output.

    Used as a Jinja2 filter to ensure CSV data doesn't crash the LaTeX compiler.
    Characters like &, %, _, $, # have special meaning in LaTeX.

    Args:
        text: Input string that may contain LaTeX special characters

    Returns:
        String with special characters escaped for LaTeX
    """
    if not isinstance(text, str):
        return str(text) if text is not None else ""

    return _LATEX_ESCAPE_PATTERN.sub(lambda m: LATEX_SPECIAL_CHARS[m.group()], text)


def parse_tags(tags_str: str) -> set[str]:
    """
    Parse pipe-separated tags string into a set.

    Args:
        tags_str: Pipe-separated tags like "ai|ml|python"

    Returns:
        Set of lowercase tag strings
    """
    if not tags_str or not isinstance(tags_str, str):
        return set()
    return {tag.strip().lower() for tag in tags_str.split("|") if tag.strip()}


def format_period_latex(period: str) -> str:
    """
    Format period string for LaTeX (ensure proper dash).

    Args:
        period: Date range like "Nov 2025 - Present"

    Returns:
        Period with proper LaTeX formatting
    """
    # Replace single dash with en-dash for proper typography
    return period.replace(" - ", " -- ").replace("–", "--")
