from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Node:
    pass

@dataclass
class Declaration(Node):
    pass

@dataclass
class Program(Node):
    classes: list["Class"] = field(default_factory=list)

    def __str__(self):
        return "".join(str(c) for c in self.classes)

@dataclass
class Identifier(Node):
    value: str

    def __str__(self):
        return self.value

@dataclass
class ClassName(Identifier):
    pass

@dataclass
class SubroutineName(Identifier):
    pass

@dataclass
class VarName(Identifier):
    pass

@dataclass
class ArrayIndex(Node):
    name: VarName
    index: "Expression"

    def __str__(self):
        return f"{self.name}[{self.index}]"

@dataclass
class Class(Node):
    name: ClassName
    classVars: list["ClassVarDec"] | None
    subroutines: list["SubroutineDec"] | None

    def __str__(self):
        """'class' className '{' classVarDec* subroutineDec* '}'"""
        parts: list[str] = []
        if self.classVars:
            parts.append("".join(str(v) for v in self.classVars))
        if self.subroutines:
            parts.append("".join(str(s) for s in self.subroutines))
        body = " ".join(parts)
        return f"class {self.name} {{ {body} }}"

@dataclass
class ClassVarDec(Declaration):
    varType: Literal['static', 'field']
    dataType: "Type"
    names: list[VarName]

    def __str__(self):
        """('static' | 'field') type varName (',' varName)* ';'"""
        vars_str = ", ".join(str(v) for v in self.names)
        return f"{self.varType} {self.dataType} {vars_str};"

@dataclass
class Type(Node):
    value: Literal['int', 'char', 'boolean'] | ClassName

    def __str__(self):
        return self.value if isinstance(self.value, str) else str(self.value)

@dataclass
class Parameter(Node):
    type: Type
    varName: VarName

    def __str__(self):
        return f"{self.type} {self.varName}"

@dataclass
class SubroutineBody(Node):
    variables: list["VarDec"] = field(default_factory=list)
    statements: list["Statement"] = field(default_factory=list)

    def __str__(self):
        variables = "".join(str(v) for v in self.variables)
        statements = "".join(str(s) for s in self.statements)
        return f"{{ {variables} {statements} }}"

@dataclass
class SubroutineDec(Declaration):
    type: Literal['constructor', 'function', 'method']
    returnType: str | Type
    name: SubroutineName
    parameters: list[Parameter]
    body: SubroutineBody

    def __str__(self):
        """('constructor' | 'function' | 'method')
        ('void' | type) subroutineName '(' parameterList ')'
        subroutineBody"""
        params = ", ".join(str(p) for p in self.parameters)
        return f"{self.type} {self.returnType} {self.name}({params}) {self.body}"

@dataclass
class VarDec(Node):
    type: Type
    names: list[VarName]

    def __str__(self):
        names_str = ", ".join(str(n) for n in self.names)
        return f"var {self.type} {names_str};"

@dataclass
class Statement(Node):
    value: "LetStatement | IfStatement | WhileStatement | DoStatement | ReturnStatement"

    def __str__(self):
        return str(self.value)

@dataclass
class LetStatement(Node):
    varName: VarName
    index: "Expression | None "
    expression: "Expression"

    def __str__(self):
        """'let' varName ('[' expression ']')? '=' expression ';'"""
        key = f"[{self.index}]" if self.index else ""
        return f"let {self.varName}{key} = {self.expression};"

@dataclass
class IfStatement(Node):
    condition: "Expression"
    statements: list[Statement]
    elseStatements: list[Statement] | None

    def __str__(self):
        """'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        if_block = "".join(str(s) for s in self.statements)
        else_block = ""
        if self.elseStatements:
            else_block_content = "".join(str(s) for s in self.elseStatements)
            else_block = f" else {{ {else_block_content} }}"
        return f"if ({self.condition}) {{ {if_block} }}{else_block}"

@dataclass
class WhileStatement(Node):
    condition: "Expression"
    statements: list[Statement]

    def __str__(self):
        """'while' '(' expression ')' '{' statements '}'"""
        statements_str = "".join(str(s) for s in self.statements)
        return f"while ({self.condition}) {{ {statements_str} }}"

@dataclass
class DoStatement(Node):
    subroutineCall: "SubroutineCall"

    def __str__(self):
        """'do' subroutineCall ';'"""
        return f"do {self.subroutineCall};"

@dataclass
class ReturnStatement(Node):
    value: "Expression | None "

    def __str__(self):
        value_str = f" {self.value}" if self.value else ""
        return f"return{value_str};"

@dataclass
class SubroutineCall(Node):
    parent: ClassName | VarName | None
    name: SubroutineName
    parameters: list["Expression"] | None

    def __str__(self):
        """subroutineName '(' expressionList ')' |
        (className | varName) '.' subroutineName '(' expressionList ')'"""
        parent = f"{self.parent}." if isinstance(self.parent, (ClassName, VarName)) else ""
        params = ", ".join(str(p) for p in self.parameters) if self.parameters else ""
        return f"{parent}{self.name}({params})"

@dataclass
class Expression(Node):
    left: "Term"
    operator: Literal['+', '-', '*', '/', '&', '|', '<', '>', '='] | None
    right: "Term | None "

    def __str__(self):
        right = f" {self.operator} {self.right}" if self.operator else ""
        return f"{self.left}{right}"

@dataclass
class Term(Node):
    unaryOp: Literal['-', '~'] | None
    value: "IntegerConstant | StringConstant | KeywordConstant \
        | VarName | ArrayIndex | SubroutineCall | Expression | Term"

    def __str__(self):
        """integerConstant | stringConstant | keywordConstant |
        varName | varName '[' expression ']' | subroutineCall |
        '(' expression ')' | unaryOp term"""
        if self.unaryOp:
            return f"{self.unaryOp}{self.value}"
        if isinstance(self.value, Expression):
            return f"({self.value})"
        return str(self.value)

@dataclass
class IntegerConstant(Node):
    value: int

    def __str__(self):
        return str(self.value)

@dataclass
class StringConstant(Node):
    value: str

    def __str__(self):
        return f'"{self.value}"'

@dataclass
class KeywordConstant(Node):
    value: Literal['true', 'false', 'null', 'this']

    def __str__(self):
        return self.value
