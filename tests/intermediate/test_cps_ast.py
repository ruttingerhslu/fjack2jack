import unittest

from fjack.ast import *
from intermediate.cps_ast import cps_transform

class TestCPSTransform(unittest.TestCase):
    def test_function_literal_to_cps(self):
        # fun (x) -> (x * 2)
        original = FunctionLiteral(
            parameters=[Identifier("x")],
            body=InfixExpression(
                left=Identifier("x"),
                operator="*",
                right=IntegerLiteral(2)
            )
        )
        # fun (x, k) -> k (x * 2)
        expected = FunctionLiteral(
            parameters=[Identifier("x"), Identifier("k")],
            body=FunctionApplication(
                function=Identifier("k"),
                argument=InfixExpression(
                    left=Identifier("x"),
                    operator="*",
                    right=IntegerLiteral(2)
                )
            )
        )

        transformed = cps_transform(original)

        self.assertEqual(transformed, expected)
