from enum import Enum
from typing import final

class TokenType(str, Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    IDENT = "IDENT"
    INT = "INT"

    ASTERISK = "*"
    MINUS = "-"
    PLUS = "+"

    LPAREN = "("
    RPAREN = ")"
    ARROW = "->"
    COMMA = ","

    # keywords
    FUNCTION = "FUNCTION"

    LAMBDA = "LAMBDA"
    IF = "IF"
    LET = "LET"
    LOOP = "LOOP"

@final
class Token:
    def __init__(self, type_: TokenType = TokenType.ILLEGAL, literal: str = ''):
        self.type = type_
        self.literal = literal

    def __eq__(self, other: object):
        if not isinstance(other, Token):
            return NotImplemented
        return self.type == other.type and self.literal == other.literal

    def __repr__(self):
        return f"Token({self.type}, {self.literal!r})"
