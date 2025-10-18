import unittest

from fjack.ast import *
from intermediate.cps_ast import cps_transform

class TestCPSTransform(unittest.TestCase):
    def test_function_literal_to_cps(self):
        # fun (x) -> (x + 1)
        expr = FunctionLiteral([Identifier("x")],
            InfixExpression(Identifier("x"), "+", IntegerLiteral(1)))

        k = Identifier("k")
        transformed = cps_transform(expr, k)
        expected = "fun (x, k) -> (fun (v1) -> (fun (v2) -> (k (v1 + v2)) 1) x)"
        self.assertEqual(str(transformed), expected)
