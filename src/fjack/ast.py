from dataclasses import dataclass, field

@dataclass
class Node:
    pass

@dataclass
class Expression(Node):
    pass

@dataclass
class Statement(Node):
    pass

@dataclass
class Program(Node):
    statements: list[Statement] = field(default_factory=list)

    def __str__(self):
            return "".join(str(s) for s in self.statements)

@dataclass
class LetStatement(Statement):
    name: "Identifier"
    value: Expression

    def __str__(self):
        return f"let {self.name} = {self.value};"

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

    def __str__(self):
        return str(self.expression)

@dataclass
class FunctionLiteral(Expression):
    parameters: list["Identifier"]
    body: Expression | None = None

    def __str__(self):
        params = ", ".join(str(p) for p in self.parameters)
        return f"fun ({params}) -> {self.body};"

@dataclass
class InfixExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

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
