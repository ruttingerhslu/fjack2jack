import unittest

from fjack.ast import *

class TestAst(unittest.TestCase):
    def test_program_to_string(self):
        program = Program(
            parameters=[Identifier("x"), Identifier("y")],
            body=PrefixExpression(operator="+", operands=[Identifier("x"), Identifier("y")])
        )

        expected = "(λ (x y) (+ x y))"
        self.assertEqual(str(program), expected)

    def test_function_call(self):
        program = Program(
            parameters=[Identifier("x")],
            body=Call(
                func=Identifier("add"),
                args=[Identifier("x"), IntegerLiteral(2)]
            )
        )

        expected = "(λ (x) (add x 2))"
        self.assertEqual(str(program), expected)
