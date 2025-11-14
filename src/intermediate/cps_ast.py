from dataclasses import dataclass

from src.fjack.ast import *

@dataclass
class X(Identifier, E):
    """variable"""

@dataclass
class BindingCps(Node):
    """(x E)"""
    var: X
    value: "E"

@dataclass
class MCps(Node):
    """
        M' ::= (E E* C) |
            (E E*)
            (k E) |
            (if E M' M') |
            (let ((x E)) M') |
            (letrec ((x P')) M')
    """
    pass

@dataclass
class CallCps(MCps):
    """(E E* C)"""
    fn: E
    args: list[E]
    cont: "C | None"

@dataclass
class JumpCps(MCps):
    """(E E*)"""
    fn: E
    args: list[E]

@dataclass
class BindingCont(MCps):
    """(k E)"""
    cont: "K"
    arg: E

@dataclass
class IfCps(MCps):
    """(if E M' M')"""
    condition: E
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
    """variable"""
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
