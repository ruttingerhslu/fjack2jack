################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import annotations
import math
import operator as op
from typing import Any

################ Types

Symbol = str            # A Lisp Symbol is implemented as a Python str
Number = int | float    # Lisp numbers

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program: str):
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))

def tokenize(s: str) -> list[str]:
    """Convert a string into a list of tokens."""
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens: list[str]):
    """Read an expression from a sequence of tokens."""
    if not tokens:
        raise SyntaxError("unexpected EOF while reading")

    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError("unexpected ')'")
    else:
        return atom(token)

def atom(token: str):
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

################ Environments

def standard_env():
    """An environment with some Scheme standard procedures."""
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': (),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': lambda f, xs: list(map(f, xs)),
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return env

class Env(dict[Symbol, Any]):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    outer: "Env | None"

    def __init__(self, parms=(), args=(), outer=None) -> None:
        super().__init__(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        if self.outer is not None:
            return self.outer.find(var)
        raise NameError(f"Undefined symbol: {var}")

global_env = standard_env()

################ Interaction: A REPL

def repl(prompt: str = "lis.py> "):
    """A prompt-read-eval-print loop."""
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp: Any) -> str:
    """Convert a Python object back into a Lisp-readable string."""
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    return str(exp)

################ Procedures

class Procedure:
    """A user-defined Scheme procedure."""
    def __init__(self, parms, body, env: Env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

def eval(x: Any, env: Env = global_env) -> Any:
    """Evaluate an expression in an environment."""
    if isinstance(x, Symbol):          # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list):      # constant literal
        return x
    elif x[0] == 'quote':              # (quote exp)
        _, exp = x
        return exp
    elif x[0] == 'if':                 # (if test conseq alt)
        _, test, conseq, alt = x
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)
    elif x[0] == 'define':             # (define var exp)
        _, var, exp = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':               # (set! var exp)
        _, var, exp = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':             # (lambda (var...) body)
        _, parms, body = x
        return Procedure(parms, body, env)
    else:                              # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)

if __name__ == "__main__":
    repl()
