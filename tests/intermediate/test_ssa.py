import unittest

from intermediate.ssa import *
from intermediate.cps_ast import *

import fjack.ast as fjack

class TestCps(unittest.TestCase):
    # def test_transform(self):
    #     """
    #         (λ_proc (x y k) (k (+ x y)))
    #     """
    #     input = Pproc(
    #         args=[X(value='x'), X(value='y')],
    #         k=K(value='k'),
    #         body=BindingCont(
    #             cont=K(value='k'),
    #             arg=PrefixExpression(operator='+', operands=[X(value='x'), X(value='y')])
    #     ))
    #     ssa = SSA()
    #     transformed = ssa.transform_g_proc(input)

    #     expected = P(
    #         args=[X_ssa(value='y'), X_ssa(value='k')],
    #         body=ReturnValue(
    #             value=E_ssa(
    #                 left=Term(unaryOp=None,
    #                     value=E_ssa(
    #                         left=Term(unaryOp=None, value=VarName(value='x')),
    #                         operator=None,
    #                         right=None)),
    #                 operator='+', right=None)),
    #         label_blocks=[
    #             L(label=Label(value='x'), phis=[I(var=X_ssa(value='y'), args=[])],
    #             body=ReturnValue(
    #                 value=E_ssa(left=Term(unaryOp=None, value=E_ssa(left=Term(unaryOp=None, value=VarName(value='x')),
    #                 operator=None, right=None)), operator='+', right=None))
    #             )])

    #     print(transformed)
    #     self.assertEqual(transformed, expected)

    def test_phi_assignments(self):
        """
            (λ_proc (k)
                (letrec ((l (λ_jump (x)
                                (if (= x 0)
                                    (k x)
                                    (l (- x 1))))))
                    (l 2)))
        """
        # λ_jump l(x)
        l_jump = Pjump(
            args=[X("x")],
            body=IfCps(
                condition=PrefixExpression("=", [X("x"), X("0")]),
                then_branch=JumpCps(fn=X("k"), args=[X("x")]),
                else_branch=JumpCps(fn=X("l"), args=[PrefixExpression(X("-"), args=[X("x"), X("1")], cont=K("k"))])
            )
        )

        # letrec ((l λ_jump ...)) (l 2)
        letrec = LetrecCps(
            bindings=[BindingRec(var=X("l"), value=l_jump)],
            body=JumpCps(fn=X("l"), args=[X("2")])
        )

        # λ_proc(k) { letrec ... }
        proc = Pproc(
            args=[X("k")],
            k=K("k"),
            body=letrec
        )

        ssa = SSA()
        transformed = ssa.transform_g_proc(input)

        for l in ssa.labeled_blocks:
            print(f"{l}: {ssa.labeled_blocks[l].phis}")
        # self.assertEqual(transformed, expected)
