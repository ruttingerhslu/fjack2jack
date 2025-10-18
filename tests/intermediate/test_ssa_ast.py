import unittest
from jack.ast import *
from intermediate.ssa_ast import  *

class TestSSAAst(unittest.TestCase):
    def test_ssa_to_jack_ast_basic(self):
        # L0(a, b):
        #   t0 = a + b
        #   return t0
        proc = SSAProcedure(
            name="L0",
            params=["a", "b"],
            body=[
                SSAStatement("t0", "a + b"),
                SSAStatement("return", "t0"),
            ]
        )

        jack_proc = ssa_to_jack_ast(proc, return_type="int")

        assert isinstance(jack_proc, SubroutineDec)
        assert jack_proc.name.value == "L0"
        assert len(jack_proc.parameters) == 2
        assert len(jack_proc.body.variables) == 1
        assert len(jack_proc.body.statements) == 2

        var_dec = jack_proc.body.variables[0]
        assert isinstance(var_dec, VarDec)
        assert var_dec.names[0].value == "t0"

        let_stmt = jack_proc.body.statements[0].value
        assert isinstance(let_stmt, LetStatement)
        assert let_stmt.varName.value == "t0"
        assert let_stmt.expression.operator == "+"

        ret_stmt = jack_proc.body.statements[1].value
        assert isinstance(ret_stmt, ReturnStatement)

        jack_str = str(jack_proc)
        assert "function int L0" in jack_str
        assert "let t0 = a + b;" in jack_str
        assert "return t0;" in jack_str

        print(jack_str)
