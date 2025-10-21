from dataclasses import dataclass
from typing import Literal

@dataclass
class Node:
    pass

@dataclass
class M(Node):
    """
        M ::= E | (E E*) | (if E M M) |
              (let ((x M)) M ) |
              (loop l ((x E)*) M) |
              (l E*)
    """
    pass

@dataclass
class E(M):
    """E ::= x | (+ E E) | ..."""
    pass

@dataclass
class Identifier(E):
    """x"""
    value: str
    def __str__(self):
        return self.value

@dataclass
class IntegerLiteral(E):
    value: int
    def __str__(self):
        return str(self.value)

@dataclass
class PrefixExpression(E):
    """(+ E E)"""
    operator: Literal['+', '-', '*', '/', '&', '|', '<', '>', '=']
    operands: list[E]
    def __str__(self):
        return f"({self.operator} {self.operands[0]} {self.operands[1]})"


@dataclass
class Call(M):
    """(E E*)"""
    func: E
    args: list[E]
    def __str__(self):
        args_str = " ".join(map(str, self.args))
        return f"({self.func} {args_str})"

@dataclass
class If(M):
    """(if E M M)"""
    condition: E
    then_branch: M
    else_branch: M
    def __str__(self):
        return f"(if {self.condition} {self.then_branch} {self.else_branch})"

@dataclass
class BindingM(Node):
    """(x M)"""
    var: Identifier
    value: M
    def __str__(self):
        return f"({self.var} {self.value})"

@dataclass
class BindingE(Node):
    """(x E)"""
    var: Identifier
    value: E
    def __str__(self):
        return f"({self.var} {self.value})"

@dataclass
class Let(M):
    """(let ((x M)) M)"""
    bindings: list[BindingM]
    body: M
    def __str__(self):
        binds = " ".join(map(str, self.bindings))
        return f"(let ({binds}) {self.body})"

@dataclass
class Loop(M):
    """(loop l ((x E)*) M)"""
    label: str
    bindings: list[BindingE]
    body: M
    def __str__(self):
        binds = " ".join(map(str, self.bindings))
        return f"(loop {self.label} ({binds}) {self.body})"

@dataclass
class LabelCall(M):
    """(l E*)"""
    label: str
    args: list[E]
    def __str__(self):
        return f"({self.label} {' '.join(map(str, self.args))})"

@dataclass
class Program(Node):
    """(λ (x*) M)"""
    parameters: list[Identifier]
    body: M
    def __str__(self):
        params = " ".join(map(str, self.parameters))
        return f"(λ ({params}) {self.body})"
