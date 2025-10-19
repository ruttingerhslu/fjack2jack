import unittest

from fjack.lexer import Lexer
from fjack.token import Token, TokenType

class TestLexer(unittest.TestCase):
    def test_next_token(self):
        input_ = '(λ (x) (+ x 1))'
        l = Lexer(input_)

        expected_tokens = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.LAMBDA, 'λ'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.INT, '1'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.EOF, ''),
        ]

        for expected in expected_tokens:
            tok = l.next_token()
            self.assertEqual(tok, expected)

if __name__ == '__main__':
    _ = unittest.main()
