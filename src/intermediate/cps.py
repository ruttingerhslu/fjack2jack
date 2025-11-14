from src.fjack.ast import *
from .cps_ast import *

class TransformError(Exception):
    """Raised when a transform error occurs."""
    pass

class CPS:
    """
        M' ::=  (E E* C) |
                (E E*) |
                (k E) |
                (if E M' M') |
                (let ((x E)) M') |
                (letrec ((x P')) M')
        C  ::=  k | (λ_cont (x) M')
        P' ::=  (λ_proc (x* k) M') |
                (λ_jump (x*) M')
        where x ∈ variables
              l ∈ labels
    """
    rec_bound: list[X]

    def __init__(self):
        self.rec_bound = []

    def transform(self):
        """
            F: M x C -> M'
            F([E, k]) = (k E)
            F([(E, (λ_cont (x) M'))]) = (let ((x E)) M')
            F([(E...), C]) = (let ((v (E ...))) (j v)) if C = x and x is bound by letrec
                           = (E ... C)                 otherwise
            F([(let ((x M_1)) M_2), C]) = F([M_1, (λ(x) F([M_2, C]))])
            F([(if E M_1 M_2), k]) = (if E F([M_1, k]) F([M_2, k]))
            F([(if E M_1 M_2), (λ_cont (x) M')]) =
                (letrec ((x (λ_jump (x) M'))) (if E F([M_1, x]) F([M_2, x])))
            F([(loop l ((x E_initial) ...)M), C]) =
                (letrec ((l (λ_jump (x...) F([M, C])))) (l E_initial ...))
            F([(l E ...), C]) = (l E ...)

            V : P -> P'
            V([(λ(x...) M)]) = (λ_proc (x...k) F([M, k]))
        """
        pass

    def transform_f(self, m: M, c: C) -> MCps:
        """F: M x C -> M'"""
        match m:
            case E():
                match c:
                    case K():
                        return BindingCont(c, m)
                    case Ccont():
                        x = c.arg
                        return LetCps([BindingCps(x, m)], c.body)
                    case _:
                        pass
            case Call():
                value = CallCps(m.func, m.args, None)
                if isinstance(c, X) and c in self.rec_bound and isinstance(value, E):
                    return LetCps(
                        [BindingCps(X("v"), value)],
                        JumpCps(Identifier("j"), [Identifier("v")])
                    )
                else:
                    return CallCps(m.func, m.args, c)
            case Let(bindings, body):
                binding = bindings[0]
                if isinstance(binding, X):
                    return self.transform_f(binding.value, Ccont(X(str(binding.var)), self.transform_f(body, c)))
            case If():
                match c:
                    case K():
                        return IfCps(m.condition, self.transform_f(m.then_branch, c), self.transform_f(m.else_branch, c))
                    case Ccont():
                        self.rec_bound.append(c.arg)
                        return LetrecCps([BindingRec(c.arg, Pjump([c.arg], c.body))],
                            IfCps(m.condition, self.transform_f(m.then_branch, c), self.transform_f(m.else_branch, c)))
                    case _:
                        pass
            case Loop(fn, args, body):
                if isinstance(fn, Identifier):
                    vars = [b.var for b in args if isinstance(b.var, X)]
                    values = [b.value for b in args]
                    self.rec_bound.append(X(fn))
                    return LetrecCps([BindingRec(X(fn), Pjump(vars, self.transform_f(body, c)))],
                        JumpCps(fn, values))
            case LabelCall():
                return JumpCps(m.label, m.args)
            case _:
                pass
        raise TransformError(f"Unhandled pattern in transform_f: {m}, {c}")

    def transform_v(self, p: Program) -> PCps:
        """V : P -> P'"""
        k = K("k")
        args = [X(str(param)) for param in p.parameters]
        return Pproc(args, k, self.transform_f(p.body, k))
