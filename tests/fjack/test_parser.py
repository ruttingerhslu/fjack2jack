import unittest

from fjack.lexer import Lexer
from fjack.parser import Parser

from fjack.ast import *

class TestParser(unittest.TestCase):
    def test_lambda(self):
        input = "(λ (x y) (+ x y))"
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(len(program.body), 1)
