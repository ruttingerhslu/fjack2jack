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

# M ::= (E E*) | (if E M M) | (let ((x M)) M) | (loop l ((x E)*) M) | (l E*)
@dataclass
class Call(M):
    func: Expression
    args: list[Expression]
    def __str__(self):
        args_str = " ".join(map(str, self.args))
        return f"({self.func} {args_str})"

@dataclass
class If(M):
    condition: Expression
    then_branch: M
    else_branch: M
    def __str__(self):
        return f"(if {self.condition} {self.then_branch} {self.else_branch})"

@dataclass
class Let(M):
    name: Identifier
    value: M
    body: M
    def __str__(self):
        return f"(let (({self.name} {self.value})) {self.body})"

@dataclass
class Loop(M):
    label: str
    bindings: list[tuple[Identifier, Expression]]
    body: M
    def __str__(self):
        binds = " ".join(f"({x} {e})" for x, e in self.bindings)
        return f"(loop {self.label} ({binds}) {self.body})"

@dataclass
class LabelCall(M):
    label: str
    args: list[Expression]
    def __str__(self):
        return f"({self.label} {' '.join(map(str, self.args))})"

# P ::= (λ (x*) M)
@dataclass
class Program(Node):
    parameters: list[Identifier]
    body: M
    def __str__(self):
        params = " ".join(map(str, self.parameters))
        return f"(λ ({params}) {self.body})"
