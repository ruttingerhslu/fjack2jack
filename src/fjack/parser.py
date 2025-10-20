from typing import final
from .ast import *
from .lexer import Lexer
from .token import Token, TokenType

class ParserError(Exception):
    """Raised when a parsing error occurs."""
    pass

@final
class Parser:
    """
        M ::=   E | (E E*) | (if E M M) |
                (let ((x M)) M ) |
                (loop l ((x E)*) M) |
                (l E*)
        E ::=   x | (+E E) | ...
        P ::=   (λ (x*) M)
        where x ∈ variables
              l ∈ labels
    """
    def __init__(self, lexer: Lexer):
        self.l = lexer
        self.curr_token: Token = Token()
        self.peek_token: Token = Token()

        # set cur and peek tokens
        self.next_token()
        self.next_token()

    # util functions
    def next_token(self) -> None:
        """Advance current and peek tokens."""
        self.curr_token = self.peek_token
        self.peek_token = self.l.next_token()

    def expect_curr(self, token_type: TokenType):
        if self.curr_token.type == token_type:
            self.next_token()
        else:
            raise ParserError(f"Expected current token {token_type}, got {self.curr_token.type} instead.")

    def expect_peek(self, token_type: TokenType):
        if self.peek_token.type == token_type:
            self.next_token()
        else:
            raise ParserError(f"Expected next token {token_type}, got {self.peek_token.type} instead.")

    # parse functions
    def parse_program(self) -> Program:
        """
            P ::= (λ (x*) M)
        """
        self.expect_curr(TokenType.LPAREN)
        self.expect_curr(TokenType.LAMBDA)
        self.expect_curr(TokenType.LPAREN)
        params: list[Identifier] = []
        while self.curr_token.type != TokenType.RPAREN:
            if self.curr_token.type != TokenType.IDENT:
                raise ParserError(f"Expected parameter name, got {self.curr_token.type}")
            params.append(Identifier(self.curr_token.literal))
            self.next_token()
        self.expect_curr(TokenType.RPAREN)
        body = self.parse_m()
        self.expect_curr(TokenType.RPAREN)
        return Program(params, body)

    def parse_m(self) -> M:
        """
            M ::= E
                | (E E*)
                | (if E M M)
                | (let ((x M)) M)
                | (loop l ((x E)*) M)
                | (l E*)
        """
        if self.curr_token.type == TokenType.LPAREN:
            return self.parse_list_form()

        e = self.parse_e()
        return e

    def parse_list_form(self) -> M:
        self.expect_curr(TokenType.LPAREN)

        if self.curr_token.type == TokenType.RPAREN:
            raise ParserError("Unexpected empty list '()'")

        match self.curr_token.type:
            case TokenType.IF:
                return self.parse_if_form()
            case TokenType.LET:
                return self.parse_let_form()
            case TokenType.LOOP:
                return self.parse_loop_form()
            case TokenType.PLUS | TokenType.MINUS | TokenType.ASTERISK | TokenType.SLASH:
                return self.parse_e()
            case _:
                # (E E*)
                func = self.parse_e()
                args: list[Expression] = []
                while self.curr_token.type != TokenType.RPAREN:
                    args.append(self.parse_e())
                self.expect_curr(TokenType.RPAREN)
                return Call(func, args)

    def parse_e(self) -> Expression:
        """E ::= x | INT | (+ E E) | ... """
        match self.curr_token.type:
            case TokenType.IDENT:
                ident = Identifier(self.curr_token.literal)
                self.next_token()
                return ident
            case TokenType.INT:
                val = IntegerLiteral(int(self.curr_token.literal, 0))
                self.next_token()
                return val
            case t if t in [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK, TokenType.SLASH]:
                op = self.curr_token.literal
                self.next_token()
                operands: list[Expression] = []
                operands.append(self.parse_e())
                operands.append(self.parse_e())
                return PrefixExpression(op, operands)
            case _:
                raise ParserError(f"Unexpected token in expression: {self.curr_token.type} ({self.curr_token.literal})")

    # special forms
    def parse_if_form(self) -> If:
        """(if E M M)"""
        self.expect_curr(TokenType.IF)
        cond = self.parse_e()
        then_branch = self.parse_m()
        else_branch = self.parse_m()
        self.expect_peek(TokenType.RPAREN)
        return If(cond, then_branch, else_branch)

    def parse_let_form(self) -> Let:
        """(let ((x M)) M)"""
        self.expect_curr(TokenType.LET)
        self.expect_curr(TokenType.LPAREN)
        self.expect_curr(TokenType.LPAREN)
        name = Identifier(self.curr_token.literal)
        self.expect_curr(TokenType.IDENT)
        value = self.parse_m()
        self.expect_curr(TokenType.RPAREN)
        self.expect_curr(TokenType.RPAREN)
        body = self.parse_m()
        self.expect_curr(TokenType.RPAREN)
        return Let(name, value, body)

    def parse_loop_form(self) -> Loop:
        """(loop l ((x E)*) M)"""
        self.expect_curr(TokenType.LOOP)
        label = self.curr_token.literal
        self.expect_curr(TokenType.IDENT)
        self.expect_curr(TokenType.LPAREN)
        bindings: list[tuple[Identifier, Expression]] = []
        while self.curr_token.type != TokenType.RPAREN:
            self.expect_curr(TokenType.LPAREN)
            bname = Identifier(self.curr_token.literal)
            self.expect_curr(TokenType.IDENT)
            bexpr = self.parse_e()
            self.expect_curr(TokenType.RPAREN)
            bindings.append((bname, bexpr))
        self.expect_curr(TokenType.RPAREN)
        body = self.parse_m()
        self.expect_curr(TokenType.RPAREN)
        return Loop(label, bindings, body)
