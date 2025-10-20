import unittest

from intermediate.cps import *
from fjack.ast import *

class TestCps(unittest.TestCase):
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
