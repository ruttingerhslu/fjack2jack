from .cps_ast import LetrecCps, MCps, LetCps, CallCps, JumpCps, X, K, Ccont, BindingCont, IfCps, PCps, Pproc, Pjump
from .ssa_ast import *

import src.fjack.ast as fjack

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
        E ::= x | E + E | ...
        where x ∈ variables
              l ∈ labels
    """

    # a labeled block l has n phi assignments with k arguments, e.g.:
    # {
    #   "l": {
    #       "x": [1, 4],
    #       "y": [2, 5],
    #       "z": [3, 6]
    #   }
    # }
    # x could be 1 or 4, meaning function l was both
    # called (in CPS) with arguments l(1, 2, 3) or l(4, 5, 6)
    labeled_blocks: dict[str, L] = {}

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
            G_proc([(λ_proc (x ...) M')]) = proc(x ... k) { G([M']) G_jump([(lamda_jump ...)]) ... }
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
                    case _:
                        pass
            case JumpCps():
                label_name = str(e_to_ssa(m.fn))
                edge_index = 0

                # lazily create placeholder if label not seen yet
                if label_name not in self.labeled_blocks:
                    # no body yet, but we know the arguments
                    phis = [I(X_ssa(f"x{i}"), []) for i in range(len(m.args))]
                    self.labeled_blocks[label_name] = L(Label(label_name), phis, None)

                block = self.labeled_blocks[label_name]
                edge_index = len(block.phis[0].args)

                # append each argument to φ list
                for i, arg in enumerate(m.args):
                    block.phis[i].args.append(e_to_ssa(arg))

                return Goto(Label(label_name), edge_index)
            case BindingCont():
                return ReturnValue(e_to_ssa(m.arg))
            case IfCps():
                return If(e_to_ssa(m.condition), self.transform_g(m.then_branch), self.transform_g(m.else_branch))
            case LetrecCps(bindings, body):
                for binding in bindings:
                    val = binding.value
                    if isinstance(val, Pjump):
                        label_name = binding.var.value

                        # if block exists, just fill in the body
                        if label_name in self.labeled_blocks:
                            block = self.labeled_blocks[label_name]
                            block.body = self.transform_g(val.body)
                        else:
                            # if not: create new labeled block with empty φ nodes
                            block = self.transform_g_jump(binding.var, val)
                            self.labeled_blocks[label_name] = block

                return self.transform_g(body)
            case _:
                pass
        raise TransformError(f"Unhandled pattern in transform_g: {m}")

    def transform_g_proc(self, p: Pproc) -> P:
        self.labeled_blocks = {}
        entry = self.transform_g(p.body)
        return P(
            [x_to_ssa(arg) for arg in p.args],
            entry,
            list(self.labeled_blocks.values()) # collected λ_jump
        )

    def transform_g_jump(self, label: X, pj: Pjump) -> L:
        """
            G_jump([j, (λ_jump (x ...) M')]) = j : x <- ɸ(E_0,0, E_0,1); ... G([M'])
        """
        phis = [I(x_to_ssa(arg), []) for arg in pj.args]
        return L(Label(label.value), phis, self.transform_g(pj.body))

def e_to_ssa(e: fjack.E) -> E_ssa:
    match e:
        case fjack.Identifier():
            return E_ssa(Term(None, VarName(e.value)), None, None)
        case fjack.IntegerLiteral():
            return E_ssa(Term(None, IntegerConstant(e.value)), None, None)
        case fjack.PrefixExpression():
            left_ssa = e_to_ssa(e.operands[0])
            right_term = Term(None, e_to_ssa(e.operands[1])) if len(e.operands) > 1 else None
            return E_ssa(Term(None, left_ssa), e.operator, right_term)
        case _:
            raise TransformError(f"Type conversion from cps to ssa failed: {e}")

def x_to_ssa(x: X | K) -> X_ssa:
    return X_ssa(x.value)
