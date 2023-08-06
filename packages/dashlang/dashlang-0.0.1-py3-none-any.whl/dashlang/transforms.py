"""Utility functions that allow to perform specific transformations on
inputs to conform them to some expect form.
"""
import html


def strip_string_quotes(string: str) -> str:
    """Transform a string which first and last characters are quotes
    into the same string stripped of these quotes. If the input string
    is not wrapped in quotes, this function returns the string unmodified.

    Args:
        string: The input string

    Returns:
        The input string stripped of the wrapping quotes.
    """
    out_string: str = string.strip('"') if string[0] == '"' else string
    return out_string.rstrip('"') if out_string[-1] == '"' else out_string


def unescape_html_string(string: str) -> str:
    """Transform the unescapes a string that has been escaped using the HTML
    escaping convention.

    Args:
        string: The input string

    Returns:
        The unescaped input string.
    """
    return html.unescape(string)
