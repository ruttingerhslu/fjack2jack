import unittest

from jack.ast import *

class TestJackAst(unittest.TestCase):
    def test_program_to_string(self):
        program = Program(classes=[
            Class(
                name=ClassName(value="Bar"),
                classVars=None,
                subroutines=[
                    SubroutineDec(
                        type="method",
                        returnType="void",
                        name=SubroutineName(value="foo"),
                        parameters=[
                            Parameter(
                                type=Type(value="int"),
                                varName=VarName(value="y"),
                            )
                        ],
                        body=SubroutineBody(
                            variables=[
                                VarDec(
                                    type=Type(value="int"),
                                    names=[VarName(value="temp")],
                                )
                            ],
                            statements=[
                                LetStatement(
                                    varName=VarName(value="temp"),
                                    index=None,
                                    expression=Expression(
                                        left=Term(
                                            unaryOp=None,
                                            value=VarName(value="y"),
                                        ),
                                        operator="+",
                                        right=Term(
                                            unaryOp=None,
                                            value=IntegerConstant(value=12),
                                        ),
                                    ),
                                )
                            ],
                        ),
                    )
                ],
            )
        ])

        expected = ("class Bar { method void foo(int y) { var int temp; let temp = y + 12; } }")
        self.assertEqual(str(program), expected)
