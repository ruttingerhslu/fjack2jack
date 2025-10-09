from dataclasses import dataclass, field

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
class Identifier():
    value: str

    def __str__(self):
        return self.value

@dataclass
class Class(Node):
    name: "ClassName"
    classVars: list["ClassVarDec"] | None
    subroutines: list["SubroutineDec"] | None

    def __str__(self):
        """'class' className '{' classVarDec* subroutineDec* '}'"""
        return f"class {self.name} {{ {self.classVars} {self.subroutines} }}"

@dataclass
class ClassName(Identifier):
    value: str

    def __str__(self):
        return self.value

@dataclass
class SubroutineName(Identifier):
    value: str

    def __str__(self):
        return self.value

@dataclass
class VarName(Identifier):
    value: str

    def __str__(self):
        return self.value

@dataclass
class ArrayIndex(Identifier):
    name: str
    index: "Expression"

    def __str__(self):
        return f"{self.name}[{self.index}]"

@dataclass
class ClassVarDec(Declaration):
    varType: str # 'static' | 'field'
    dataType: type
    names: list["Identifier"]

    def __str__(self):
        """('static' | 'field') type varName (',' varName)* ';'"""
        vars = ", ".join(str(v) for v in self.names)
        return f"{self.varType} {self.dataType} {vars};"

@dataclass
class Type:
    value: str | ClassName  # str: 'int' | 'char' | 'boolean'

    def __str__(self):
        return self.value if isinstance(self.value, str) else self.value.value

@dataclass
class SubroutineDec(Declaration):
    type: str # str: 'constructor' | 'function' | 'method'
    returnType: str | Type # str: 'void'
    name: SubroutineName
    parameters: list["Parameter"]
    body: "SubroutineBody"

    def __str__(self):
        """('constructor' | 'function' | 'method')
        ('void' | type) subroutineName '(' parameterList ')'
        subroutineBody"""
        params = ", ".join(str(p) for p in self.parameters)
        return f"{self.type} {self.returnType} {self.name} ({params}) {self.body}"

@dataclass
class Parameter:
    type: Type
    varName: VarName

    def __str__(self):
        return f"{self.type} {self.varName}"

@dataclass
class SubroutineBody:
    variables: list["VarDec"]
    statements: list["Statement"]

    def __str__(self):
        variables = "".join(str(s) for s in self.variables)
        statements = "".join(str(s) for s in self.statements)
        return f"{{ {variables} {statements} }}"

@dataclass
class VarDec:
    type: Type
    names: list["VarName"]

    def __str__(self):
        return f"var {self.type} {self.names[0]}"

@dataclass
class Statement:
    type: "LetStatement | IfStatement | WhileStatement | DoStatement | ReturnStatement"

    def __str__(self):
        return str(self.type)

@dataclass
class LetStatement:
    varName: VarName
    index: "Expression | None"
    expression: "Expression"

    def __str__(self):
        """'let' varName ('[' expression ']')? '=' expression ';'"""
        key = f"[{self.index}]" if self.index else ""
        return f"let {self.varName.value}{key} = {self.expression};"

@dataclass
class IfStatement:
    condition: "Expression"
    statements: list["Statement"]
    elseStatements: list["Statement"] | None

    def __str__(self):
        """'if' '(' expression ')' '{' statements '}'
            ('else' '{' statements '}')?"""
        if_block = "".join(str(s) for s in self.statements)
        else_block = ""
        if self.elseStatements:
            else_block_content = "".join(str(s) for s in self.elseStatements)
            else_block = f" else {{ {else_block_content} }}"
        return f"if ({self.condition}) {{ {if_block} }}{else_block}"

@dataclass
class WhileStatement:
    condition: "Expression"
    statements: list["Statement"]

    def __str__(self):
        """'while' '(' expression ')' '{' statements '}"""
        statements = "".join(str(s) for s in self.statements)
        return f"while ({self.condition}) {{ {statements} }}"

@dataclass
class DoStatement:
    subroutineCall: "SubroutineCall"

    def __str__(self):
        """'do' subroutineCall ';'"""
        return f"do {self.subroutineCall};"

@dataclass
class SubroutineCall:
    parent: ClassName | VarName | None
    name: SubroutineName
    parameters: list["Expression"] | None

    def __str__(self):
        """subroutineName '(' expressionList ')' | (className |
        varName) '.' subroutineName '(' expressionList ')'"""
        parent = f"{self.parent.value}." if isinstance(self.parent, (ClassName, VarName)) else ""
        if self.parameters:
            params = ", ".join(str(p) for p in self.parameters)
        else:
            params = ""
        return f"{parent}{self.name}({params})"

@dataclass
class ReturnStatement:
    value: "Expression | None"

    def __str__(self):
        return f"return {self.value};"

@dataclass
class Expression:
    left: "Term"
    operator: str | None # '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    right: "Term | None"

    def __str__(self):
        right = f"{self.operator} {self.right}" if self.operator else ""
        return f"{self.left} {right}"

@dataclass
class Term:
    unaryOp: str | None # '-', '~'
    type: "IntegerConstant | StringConstant | KeywordConstant \
    | VarName | ArrayIndex | SubroutineCall | Expression | Term"

    def __str__(self):
        """integerConstant | stringConstant | keywordConstant |
        varName | varName '[' expression ']' | subroutineCall |
        '(' expression ')' | unaryOp term"""
        prefix, postfix = ""
        match self.type:
            case ArrayIndex():
                prefix = "["
                postfix = "]"
            case Expression():
                prefix = "("
                postfix = ")"
            case Term():
                prefix = self.unaryOp
            case _:
                pass
        return f"{prefix}{self.type}{postfix}"

@dataclass
class IntegerConstant:
    value: int
    def __str__(self):
        return str(self.value)

@dataclass
class StringConstant:
    value: str
    def __str__(self):
        return self.value

@dataclass
class KeywordConstant:
    value: str # 'true' | 'false' | 'null' | 'this'
    def __str__(self):
        return self.value
