from dataclasses import dataclass

@dataclass
class Node:
    pass

@dataclass
class M(Node):
    pass

@dataclass
class Expression(M):
    pass

# E ::= x | (+ E E) | ...
@dataclass
class Identifier(Expression):
    value: str
    def __str__(self):
        return self.value

@dataclass
class IntegerLiteral(Expression):
    value: int
    def __str__(self):
        return str(self.value)

@dataclass
class PrefixExpression(Expression):
    operator: str
    operands: list[Expression]
    def __str__(self):
        return f"({self.operator} {self.operands[0]} {self.operands[1]})"

@dataclass
class Call(M):
    """(E E*)"""
    func: Expression
    args: list[Expression]
    def __str__(self):
        args_str = " ".join(map(str, self.args))
        return f"({self.func} {args_str})"

@dataclass
class If(M):
    """(if E M M)"""
    condition: Expression
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
    value: Expression
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
    args: list[Expression]
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
