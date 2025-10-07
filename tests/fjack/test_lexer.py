import unittest

from fjack.lexer import Lexer
from fjack.token import Token, TokenType

class TestLexer(unittest.TestCase):
    def test_next_token(self):
        input_ = 'fun x -> x * 2;'
        l = Lexer(input_)

        expected_tokens = [
            Token(TokenType.FUNCTION, 'fun'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.ARROW, '->'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.ASTERISK, '*'),
            Token(TokenType.INT, '2'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.EOF, ''),
        ]

        for expected in expected_tokens:
            tok = l.next_token()
            self.assertEqual(tok, expected)

if __name__ == '__main__':
    _ = unittest.main()
