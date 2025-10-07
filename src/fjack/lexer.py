from typing import final

from .token import Token, TokenType

keywords = {
    "fun": TokenType.FUNCTION,
}

def lookup_ident(ident: str) -> TokenType:
    """
    Looks up whether an identifier is a keyword.
    Returns the corresponding TokenType if found, else TokenType.IDENT.
    """
    return keywords.get(ident, TokenType.IDENT)

@final
class Lexer():
    input: str
    position: int
    read_position: int
    ch: str
    def __init__(self, input: str):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = ''
        self.read_char()

    def read_char(self):
        """Reads the next character and advances positions."""
        if self.read_position >= len(self.input):
            self.ch = '\0'
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self) -> str:
        """Reads the next character without advancing."""
        if self.read_position >= len(self.input):
            return '\0'
        else:
            return self.input[self.read_position]

    def next_token(self) -> Token:
        """Returns current character as token and advance to next."""
        token = Token()

        self.skip_whitespace()

        match self.ch:
            case '*':
                token = Token(TokenType.ASTERISK, self.ch)
            case '-':
                if self.peek_char() == '>':
                    ch = self.ch
                    self.read_char()
                    literal = ch + self.ch
                    token = Token(TokenType.ARROW, literal)
                else:
                    token = Token(TokenType.MINUS, self.ch)
            case ';':
                token = Token(TokenType.SEMICOLON, self.ch)
            case '\0':
                token = Token(TokenType.EOF, '')
            case _:
                if self.is_letter(self.ch):
                    literal = self.read_identifier()
                    type = lookup_ident(literal)
                    return Token(type, literal)
                elif self.ch.isdigit():
                    type = TokenType.INT
                    literal = self.read_number()
                    return Token(type, literal)
                else:
                    print(self.ch)
                    token = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return token

    def skip_whitespace(self):
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()

    def read_identifier(self) -> str:
        """Reads an identifier from the input."""
        position = self.position
        while self.is_letter(self.ch):
            self.read_char()
        return self.input[position:self.position]

    def read_number(self) -> str:
        """Reads a number from the input."""
        position = self.position
        while self.ch.isdigit():
            self.read_char()
        return self.input[position:self.position]

    def is_letter(self, ch: str) -> bool:
        """Returns true if the provided character is a letter."""
        return 'a' <= ch and ch <= 'z' or 'A' <= ch and ch <= 'Z' or ch == '_'

    def __iter__(self):
        return self

    def __next__(self):
        tok = self.next_token()
        if tok.type == TokenType.EOF:
            raise StopIteration
        return tok
