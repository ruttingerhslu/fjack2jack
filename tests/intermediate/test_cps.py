import unittest

from src.intermediate.cps import *
from src.fjack.ast import *

class TestCps(unittest.TestCase):
    """
        (λ (x y) (+ x y)) to
        (λ_proc (x y k) (k (+ x y)))
    """
    def test_transform(self):
        input = Program(
            parameters=[Identifier("x"), Identifier("y")],
            body=PrefixExpression(operator="+", operands=[Identifier("x"), Identifier("y")])
        )
        cps = CPS()
        transformed = cps.transform_v(input)

        expected = Pproc(
            args=[X(value='x'), X(value='y')],
            k=K(value='k'),
            body=BindingCont(
                cont=K(value='k'),
                arg=PrefixExpression(operator='+', operands=[Identifier(value='x'), Identifier(value='y')])
            ))

        self.assertEqual(transformed, expected)

    def test_integer(self):
        input = Program(
            parameters=[Identifier("x")],
            body=PrefixExpression(operator="+", operands=[Identifier("x"), IntegerLiteral(1)])
        )
        cps = CPS()
        transformed = cps.transform_v(input)

        expected = Pproc(
            args=[X(value='x')],
            k=K(value='k'),
            body=BindingCont(
                cont=K(value='k'),
                arg=PrefixExpression(operator='+', operands=[Identifier(value='x'), IntegerLiteral(value=1)])
            ))

        self.assertEqual(transformed, expected)
