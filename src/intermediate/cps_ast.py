from dataclasses import dataclass

from fjack.ast import *

@dataclass
class X(Identifier):
    """variables"""
    pass

@dataclass
class BindingCps(Node):
    """(x E)"""
    var: X
    value: "Expression | MCps"

@dataclass
class BindingCall(Node):
    """(x (E E*))"""
    var: X
    fn: Expression
    args: list[Expression]

@dataclass
class MCps(Node):
    """
        M' ::= (E E* C) |
            (k E) |
            (if E M' M') |
            (let ((x E)) M') |
            (letrec ((x P')) M')
    """
    pass

@dataclass
class CallCps(MCps):
    """(E E* C)"""
    fn: Expression
    args: list[Expression]
    cont: "C | None"

@dataclass
class BindingCont(MCps):
    """(k E)"""
    cont: "K"
    arg: Expression

@dataclass
class IfCps(MCps):
    """(if E M' M')"""
    condition: Expression
    then_branch: MCps
    else_branch: MCps
    def __str__(self):
        return f"(if {self.condition} {self.then_branch} {self.else_branch})"

@dataclass
class LetCps(MCps):
    """(let ((x E)) M')"""
    bindings: list[BindingCps]
    body: MCps

@ dataclass
class BindingRec(Node):
    """(x P')"""
    var: X
    value: "PCps"

@dataclass
class LetrecCps(MCps):
    """(letrec ((x P')) M')"""
    bindings: list[BindingRec]
    body: MCps

@dataclass
class C(Node):
    """C ::= k | (λ_cont (x) M')"""
    pass

@dataclass
class K(C, Identifier):
    """labels"""
    pass

@dataclass
class Ccont(C):
    """(λ_cont (x) M')"""
    arg: X
    body: MCps

@dataclass
class PCps(Node):
    """
        P' ::= (λ_proc (x* k) M') |
               (λ_jump (x*) M')
    """
    pass

@dataclass
class Pproc(PCps):
    """(λ_proc (x* k) M')"""
    args: list[X]
    k: K
    body: MCps

@dataclass
class Pjump(PCps):
    """(λ_jump (x*) M')"""
    args: list[X]
    body: MCps
