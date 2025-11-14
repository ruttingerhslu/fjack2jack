import unittest

from src.intermediate.ssa import *
from src.intermediate.cps_ast import *

import src.fjack.ast as fjack

class TestCps(unittest.TestCase):
    def test_transform(self):
        """
            (λ_proc (x y k) (k (+ x y)))
        """
        input = Pproc(
            args=[X(value='x'), X(value='y')],
            k=K(value='k'),
            body=BindingCont(
                cont=K(value='k'),
                arg=PrefixExpression(operator='+', operands=[X(value='x'), X(value='y')])
        ))
        ssa = SSA()
        transformed = ssa.transform_g_proc(input)

        expected = P(
            args=[X_ssa(value='y'), X_ssa(value='k')],
            body=ReturnValue(
                value=E_ssa(
                    left=Term(unaryOp=None,
                        value=E_ssa(
                            left=Term(unaryOp=None, value=VarName(value='x')),
                            operator=None,
                            right=None)),
                    operator='+', right=None)),
            label_blocks=[
                L(label=Label(value='x'), phis=[I(var=X_ssa(value='y'), args=[])],
                body=ReturnValue(
                    value=E_ssa(left=Term(unaryOp=None, value=E_ssa(left=Term(unaryOp=None, value=VarName(value='x')),
                    operator=None, right=None)), operator='+', right=None))
                )])

        print(transformed)
        self.assertEqual(transformed, expected)
