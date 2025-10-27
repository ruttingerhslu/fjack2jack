from dataclasses import dataclass

from jack.ast import *

@dataclass
class Label(Identifier):
    """label"""

@dataclass
class E_ssa(Expression):
    """x | E+ E | ..."""
    pass

@dataclass
class X_ssa(Identifier):
    """variable"""
    value: str

@dataclass
class I(Node):
    """x <- ɸ(E*);"""
    var: X_ssa
    args: list[E_ssa]

@dataclass
class ProcedureCall(Node):
    """E(E*)"""
    func: E_ssa
    args: list[E_ssa]

@dataclass
class Block(Node):
    """
        B ::= x <- E; B | x <- E(E*); B |
              goto l_i; |
              return E; | return E(E*); |
              if E then B else B
    """
    pass

@dataclass
class AssignmentBlock(Block):
    """x <- E; B"""
    var: X_ssa
    value: E_ssa
    body: Block

@dataclass
class AssignmentCallBlock(Block):
    """x <- E(E*); B"""
    var: X_ssa
    value: ProcedureCall
    body: Block

@dataclass
class Goto(Block):
    """goto l_i;"""
    label: Label

@dataclass
class ReturnValue(Block):
    """return E;"""
    value: E_ssa

@dataclass
class ReturnCall(Block):
    """return E(E*);"""
    call: ProcedureCall

@dataclass
class If(Block):
    """if E then B else B"""
    condition: E_ssa
    then_block: Block
    else_block: Block

@dataclass
class L(Node):
    """l : I* B"""
    label: Label
    phi_funcs: list[I]
    body: Block

@dataclass
class P(Node):
    """P ::= proc(x*) {B L*}"""
    args: list[X_ssa]
    body: Block
    label_blocks: list[L]
