from .cps_ast import LetrecCps, MCps, LetCps, CallCps, X, K, Ccont, BindingCont, IfCps, PCps, Pproc, Pjump
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

    def transform(self):
        """
            G: M' -> B
            G([(let ((x E)) M')]) = x <- E; G([M'])
            G([(E ... (λ_cont (x) M'))]) = x <- E(...); G([M'])
            G([(E...k)]) = return E(...);
            G([(k E)]) = return E;
            G([(j E_0,i E_1,i ...)]) = goto j_i;
            G([(if E M_1' M_2')]) = if E then G([M_1']) else G([M_2'])
            G([(letrec (...) M')]) = G([M'])
            G_proc : P' -> P
            G_proc([(λ_proc (x ...) M')]) = proc(x ... k) { G([M']) }
            G_jump : j x (λ_jump (x ...) M') -> L
            G_jump([j, (λ_jump (x ...) M')]) = j : x <- ɸ(E_0,0, E_0,1); ... G([M'])
        """
        pass

    def transform_g(self, m: MCps) -> Block:
        """G: M' -> B"""
        match m:
            case LetCps():
                binding = m.bindings[0]
                return AssignmentBlock(x_to_ssa(binding.var), e_to_ssa(binding.value), self.transform_g(m))
            case CallCps():
                match m.cont:
                    case Ccont():
                        return AssignmentCallBlock(
                            x_to_ssa(m.cont.arg),
                            ProcedureCall(e_to_ssa(m.fn), list(map(e_to_ssa, m.args))),
                            self.transform_g(m.cont.body)
                        )
                    case K():
                        return ReturnCall(ProcedureCall(e_to_ssa(m.fn), list(map(e_to_ssa, m.args))))
                    case None:
                        return Goto(Label(str(e_to_ssa(m.fn))))
                    case _:
                        pass
            case BindingCont():
                return ReturnValue(e_to_ssa(m.arg))
            case IfCps():
                return If(e_to_ssa(m.condition), self.transform_g(m.then_branch), self.transform_g(m.else_branch))
            case LetrecCps():
                return self.transform_g(m.body)
            case _:
                pass
        raise TransformError(f"Unhandled pattern in transform_g: {m}")

    def transform_g_proc(self, p: PCps) -> P:
        if isinstance(p, Pproc):
            j = p.args[0]
            args = [x_to_ssa(arg) for arg in p.args[1:]] + [x_to_ssa(p.k)]
            return P(
                args,
                self.transform_g(p.body),
                [self.transform_g_jump(j, Pjump(p.args[1:], p.body))]
            )
        raise TransformError(f"Unhandled pattern in transform_g_proc: {p}")

    def transform_g_jump(self, j: X, pj: Pjump) -> L:
        return L(Label(j.value), [I(x_to_ssa(pj.args[0]), list(map(e_to_ssa, pj.args[1:])))], self.transform_g(pj.body))

def e_to_ssa(e: fjack.E) -> E_ssa:
    match e:
        case fjack.Identifier():
            return E_ssa(Term(None, VarName(e.value)), None, None)
        case fjack.IntegerLiteral():
            return E_ssa(Term(None, IntegerConstant(e.value)), None, None)
        case fjack.PrefixExpression():
            left_ssa = e_to_ssa(e.operands[0])
            return E_ssa(Term(None, left_ssa), e.operator, None)
        case _:
            raise TransformError(f"Type conversion from cps to ssa failed: {e}")

def x_to_ssa(x: X | K) -> X_ssa:
    return X_ssa(x.value)
