from dataclasses import dataclass
import re
from typing import cast, Literal

from jack.ast import *

@dataclass
class SSAStatement:
    target: str
    expr: str

@dataclass
class SSAProcedure:
    name: str
    params: list[str]
    body: list[SSAStatement]

def ssa_to_jack_ast(ssa_proc: SSAProcedure, return_type: str = "int") -> SubroutineDec:
    local_vars = [VarDec(Type("int"), [VarName(stmt.target)])
                  for stmt in ssa_proc.body if stmt.target != "return"]

    statements: list[Statement] = []
    for stmt in ssa_proc.body:
        if stmt.target == "return":
            statements.append(Statement(ReturnStatement(Expression(Term(None, VarName(stmt.expr)), None, None))))
        else:
            if any(op in stmt.expr for op in ['+', '-', '*', '/', '&', '|', '<', '>', '=']):
                left_str, op, right_str = parse_infix(stmt.expr)  # helper function
                op = cast(Literal['+', '-', '*', '/', '&', '|', '<', '>', '='], op)
                expr = Expression(Term(None, VarName(left_str)), op, Term(None, VarName(right_str)))
            else:
                expr = Expression(Term(None, VarName(stmt.expr)), None, None)
            statements.append(Statement(LetStatement(VarName(stmt.target), None, expr)))

    body = SubroutineBody(variables=local_vars, statements=statements)

    return SubroutineDec(
        type="function",
        returnType=return_type,
        name=SubroutineName(ssa_proc.name),
        parameters=[Parameter(Type("int"), VarName(p)) for p in ssa_proc.params],
        body=body
    )

def parse_infix(expr: str) -> tuple[str, str, str]:
    """
    Parse a simple infix expression like 'a + b' or 't1 * t2'
    into (left, operator, right).
    Works only for single binary operators.
    """
    match = re.match(r"^\s*([A-Za-z0-9_]+)\s*([\+\-\*/&|<>=])\s*([A-Za-z0-9_]+)\s*$", expr)
    if not match:
        raise ValueError(f"Unsupported infix expression: {expr}")
    left, op, right = match.groups()
    return left, op, right
