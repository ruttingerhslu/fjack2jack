import unittest

from fjack.ast import *

class TestAst(unittest.TestCase):
    def test_program_to_string(self):
        program = Program(body=[
            Lambda(
                parameters=[Identifier("x"), Identifier("y")],
                body=PrefixExpression(operator="+", operands=[Identifier("x"), Identifier("y")])
            )
        ])

        expected = "(λ (x y) (+ x y))"
        self.assertEqual(str(program), expected)
