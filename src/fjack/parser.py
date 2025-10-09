from typing import Callable

from fjack.ast import *
from .lexer import Lexer
from .token import Token, TokenType

LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7
INDEX = 8

PRECEDENCES = {
    TokenType.MINUS: SUM,
    TokenType.PLUS: SUM,
    TokenType.ASTERISK: PRODUCT,
}

class ParserError(Exception):
    """Raised when a parsing error occurs."""
    pass

class Parser():
    l: Lexer

    errors: list[str]

    cur_token: Token
    peek_token: Token

    prefix_parse_fns: dict[TokenType, Callable[[], Expression]] = {}
    infix_parse_fns: dict[TokenType, Callable[[Expression], Expression]] = {}

    def __init__(self, lexer: Lexer):
        self.l = lexer

        self.errors = []

        # set both current and peek token
        self.peek_token = Token()
        self.next_token()
        self.next_token()

        # register prefix and infix fns
        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.FUNCTION, self.parse_function_literal)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)

        self.register_infix(TokenType.ASTERISK, self.parse_infix_expr)
        self.register_infix(TokenType.PLUS, self.parse_infix_expr)
        self.register_infix(TokenType.MINUS, self.parse_infix_expr)

    def register_prefix(self, token_type: TokenType, fn: Callable[[], Expression]):
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type: TokenType, fn: Callable[[Expression], Expression]):
        self.infix_parse_fns[token_type] = fn

    def next_token(self):
        """Advances to the next token; updating current and peek token."""
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def consume(self, token_type: TokenType):
        """Checks if next token meets expectation and if so advances."""
        if self.peek_token.type == token_type:
            self.next_token()
        else:
            raise ParserError(f"Expected next token to be {self.cur_token.type}, \
                got {self.peek_token.type} instead.")

    def parse_program(self) -> Program:
        program = Program()
        while self.cur_token != TokenType.EOF:
            expression = self.parse_expression(LOWEST)
            program.expressions.append(expression)
            if self.peek_token.type == TokenType.EOF:
                break
            self.next_token()
        return program

    def parse_expression(self, precedence: int) -> Expression:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            raise ParserError(f"No prefix parse function for {self.cur_token.literal} found.")
        left_expr = prefix()
        while precedence < self.peek_precedence() or (
            precedence == self.peek_precedence() and self.peek_token == TokenType.ARROW
        ):
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_expr

            self.next_token()
            left_expr = infix(left_expr)

        return left_expr

    def parse_infix_expr(self, left: Expression) -> Expression:
        operator = self.cur_token.literal
        precedence = self.cur_precedence()
        self.next_token()
        right = self.parse_expression(precedence)
        return InfixExpression(left, operator, right)

    def cur_precedence(self) -> int:
        return PRECEDENCES.get(self.cur_token.type, LOWEST)

    def peek_precedence(self) -> int:
        return PRECEDENCES.get(self.peek_token.type, LOWEST)

    def parse_identifier(self) -> Identifier:
        """Parse identifier: some_identifier"""
        return Identifier(self.cur_token.literal)

    def parse_integer_literal(self) -> IntegerLiteral:
        """Parse integer literal: 42"""
        return IntegerLiteral(int(self.cur_token.literal, 0))

    def parse_function_literal(self) -> FunctionLiteral:
        """Parse function literal: fun (params) -> expr"""
        lit = FunctionLiteral(parameters=[], body=None)

        self.consume(TokenType.LPAREN)

        lit.parameters = self.parse_function_parameters()

        self.consume(TokenType.ARROW)

        self.next_token()
        lit.body = self.parse_expression(LOWEST)

        return lit

    def parse_function_parameters(self) -> list[Identifier]:
        """Parse parameters: (x, y, ...)"""
        identifiers: list[Identifier] = []

        if self.peek_token.type == TokenType.RPAREN:
            self.next_token()
            return identifiers

        self.next_token()
        identifiers.append(Identifier(self.cur_token.literal))

        while self.peek_token.type == TokenType.COMMA:
            self.next_token()
            self.next_token()
            identifiers.append(Identifier(self.cur_token.literal))

        if not self.consume(TokenType.RPAREN):
            return []

        return identifiers
