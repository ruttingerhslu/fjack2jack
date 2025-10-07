from enum import Enum
from typing import final
from typing_extensions import override

class TokenType(str, Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    IDENT = "IDENT"
    INT = "INT"

    ARROW = "->"
    ASTERISK = "*"
    MINUS = "-"

    SEMICOLON = ";"

    # keywords
    FUNCTION = "FUNCTION"

@final
class Token:
    def __init__(self, type_: TokenType = TokenType.ILLEGAL, literal: str = ''):
        self.type = type_
        self.literal = literal

    @override
    def __eq__(self, other: object):
        if not isinstance(other, Token):
            return NotImplemented
        return self.type == other.type and self.literal == other.literal

    @override
    def __repr__(self):
        return f"Token({self.type}, {self.literal!r})"
