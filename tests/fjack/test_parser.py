import unittest

from fjack.lexer import Lexer
from fjack.parser import Parser

from fjack.ast import *

class TestParser(unittest.TestCase):
    def test_function_literal(self):
        input = "fun (x) -> x * 2;"
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
