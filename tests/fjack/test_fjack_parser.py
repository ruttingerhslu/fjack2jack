import unittest

from fjack.lexer import Lexer
from fjack.parser import Parser

from fjack.ast import *

class TestParser(unittest.TestCase):
    def test_function_literal(self):
        # fun (x) -> (x + 1)
        input = "fun (x) -> (x * 2)"
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(len(program.expressions), 1)

    def test_nested_function(self):
        input = "fun (x) -> (fun (y) -> (x + y))"
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(len(program.expressions), 1)
