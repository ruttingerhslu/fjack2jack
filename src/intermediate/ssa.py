from .cps_ast import MCps, LetCps
from .ssa_ast import *

import fjack.ast as fjack

class TransformError(Exception):
    """Raised when a transform error occurs."""
    pass

class SSA:
    """
        P ::= proc(x*) {B L*}
        L ::= l : I* B
        I ::= x <- ɸ(E*);
        B ::= x <- E; B | x <- E(E*); B |
              goto l_i; |
              return E; | return E(E*); |
              if E then B else B
        E ::= x | E+ E | ...
        where x ∈ variables
              l ∈ labels
    """

    def __init__(self):
        pass

    def transform_g(self, m: MCps) -> Block:
        """G: M' -> B"""
        match m:
            case LetCps():
                binding = m.bindings[0]
                return AssignmentBlock(binding.var.to_ssa(), to_ssa(binding.value), self.transform_g(m))
            case _:
                raise TransformError(f"Unhandled pattern in transform_g: {m}")

def to_ssa(n: fjack.Node) -> E_ssa:
    match n:
        case fjack.Identifier():
            return E_ssa(Term(None, VarName(n.value)), None, None)
        case fjack.IntegerLiteral():
            return E_ssa(Term(None, IntegerConstant(n.value)), None, None)
        case fjack.PrefixExpression():
            left_ssa = to_ssa(n.operands[0])
            return E_ssa(Term(None, left_ssa), n.operator, None)
        case _:
            raise TransformError(f"Type conversion from cps to ssa failed: {n}")
