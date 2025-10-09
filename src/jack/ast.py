from dataclasses import dataclass, field

@dataclass
class Node:
    pass

@dataclass
class Class(Node):
    pass

@dataclass
class Declaration(Node):
    pass

@dataclass
class Program(Node):
    classes: list[Class] = field(default_factory=list)

    def __str__(self):
        return "".join(str(c) for c in self.classes)

@dataclass
class Identifier():
    value: str

    def __str__(self):
        return self.value

@dataclass
class ClassName(Identifier):
    value: str

@dataclass
class SubroutineName(Identifier):
    value: str

@dataclass
class VarName(Identifier):
    value: str

@dataclass
class ArrayIndex(Identifier):
    name: str
    index: "Expression"

@dataclass
class ClassVarDec(Declaration):
    type: str # 'static' | 'field'
    names: list["Identifier"]

@dataclass
class Type:
    value: str | ClassName  # str: 'int' | 'char' | 'boolean'

@dataclass
class SubroutineDec(Declaration):
    type: str # str: 'constructor' | 'function' | 'method'
    returnType: str | Type # str: 'void'
    name: SubroutineName
    parameters: list["VarName"]
    body: "SubroutineBody"

@dataclass
class SubroutineBody:
    variables: list["VarDec"]
    statements: list["Statement"]

@dataclass
class VarDec:
    type: Type
    names: list["VarName"]

@dataclass
class Statement:
    type: "LetStatement"

@dataclass
class LetStatement:
    varName: VarName
    index: "Expression | None"
    expression: "Expression"

@dataclass
class IfStatement:
    condition: "Expression"
    statements: list["Statement"]
    elseStatement: list["Statement"] | None

@dataclass
class WhileStatement:
    condition: "Expression"
    statements: list["Statement"]

@dataclass
class DoStatement:
    subroutineCall: "SubroutineCall"

@dataclass
class SubroutineCall:
    parent: ClassName | VarName | None
    name: SubroutineName
    parameters: list["Expression"] | None

@dataclass
class ReturnStatement:
    value: "Expression | None"

@dataclass
class Expression:
    left: "Term"
    operator: str | None # '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    right: "Expression | None"

@dataclass
class Term:
    unaryOp: str | None # '-', '~'
    type: "IntegerConstant | StringConstant | KeywordConstant \
    | VarName | ArrayIndex | SubroutineCall | Expression | Term"

@dataclass
class IntegerConstant:
    value: int

@dataclass
class StringConstant:
    value: str

@dataclass
class KeywordConstant:
    value: str # 'true' | 'false' | 'null' | 'this'
