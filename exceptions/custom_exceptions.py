class ParsingError(Exception):
    """Raised when a file cannot be parsed."""
    pass


class UnsupportedFileFormatError(Exception):
    """Raised when the file format is not supported by the parser."""
    pass