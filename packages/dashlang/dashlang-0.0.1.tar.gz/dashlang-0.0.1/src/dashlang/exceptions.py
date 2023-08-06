"""Exceptions raised by dashlang."""


class MismatchedTagsError(Exception):
    """Exception raised when during the parsing of the markup format, the parser
    finds a start and close tag pair whose tag name is mismatched.
    """
