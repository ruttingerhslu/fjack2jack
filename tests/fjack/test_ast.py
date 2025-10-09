import unittest

from fjack.ast import *

class TestAst(unittest.TestCase):
    def test_program_to_string(self):
        program = Program(expressions=[
            FunctionLiteral(
                parameters=[Identifier("x")],
                body=InfixExpression(
                    left=Identifier("x"),
                    operator="*",
                    right=IntegerLiteral(2)
                )
            )
        ])

        expected = "fun (x) -> (x * 2)"
        self.assertEqual(str(program), expected)
