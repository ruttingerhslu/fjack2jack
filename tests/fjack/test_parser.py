import unittest

from src.fjack.lexer import Lexer
from src.fjack.parser import Parser

from src.fjack.ast import *

class TestParser(unittest.TestCase):
    def test_lambda(self):
        input = "(λ (x y) (+ x y))"
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()

        expected = Program(
            parameters=[Identifier("x"), Identifier("y")],
            body=PrefixExpression(operator="+", operands=[Identifier("x"), Identifier("y")])
        )

        self.assertEqual(program, expected)

    def test_function_call(self):
        input = "(λ (x) (add x 2))"
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()

        expected = Program(
            parameters=[Identifier("x")],
            body=Call(
                func=Identifier("add"),
                args=[Identifier("x"), IntegerLiteral(2)]
            )
        )

        self.assertEqual(program, expected)
