import unittest

from fjack.ast import *
from intermediate.cps_to_ssa import cps_to_ssa

class TestCPStoSSA(unittest.TestCase):
    def test_function_literal_cps_to_ssa(self):
        cps_expr = FunctionLiteral(
            [Identifier("x"), Identifier("k")],
            FunctionApplication(
                Identifier("k"),
                InfixExpression(Identifier("x"), "+", IntegerLiteral(1))
            )
        )

        procs, final_var = cps_to_ssa(cps_expr)

        self.assertEqual(len(procs), 1)
        proc = procs[0]

        self.assertTrue(proc.name.startswith("L"))
        self.assertEqual(proc.params, ["x", "k"])

        self.assertEqual(len(proc.body), 4)
        self.assertEqual(proc.body[0].target, "t0")
        self.assertEqual(proc.body[0].expr, "1")
        self.assertEqual(proc.body[1].target, "t1")
        self.assertEqual(proc.body[1].expr, "x + t0")
        self.assertEqual(proc.body[2].target, "t2")
        self.assertEqual(proc.body[2].expr, "k(t1)")
        self.assertEqual(proc.body[3].target, "return")
        self.assertEqual(proc.body[3].expr, "t2")

        self.assertEqual(final_var, "t3")
