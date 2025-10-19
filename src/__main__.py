import code
from typing_extensions import override

from fjack.lexer import Lexer
from fjack.parser import Parser
from intermediate.cps_ast import cps_transform
from intermediate.cps_to_ssa import cps_to_ssa
from intermediate.ssa_ast import ssa_to_jack_ast

from fjack.ast import Identifier, FunctionLiteral

class Repl(code.InteractiveConsole):
    @override
    def runsource(self, source: str, filename: str="<input>", symbol: str="single"):
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()

        cps_program = self.to_cps(program)

        ssa_program = self.to_ssa(cps_program)

        jack_ast = self.to_jack(ssa_program)

        print(str(jack_ast))

        for token in lexer:
            print(token)
        return True

    def to_cps(self, program):
        new_exprs = []
        for expr in program.expressions:
            k = Identifier("k")
            identity_k = FunctionLiteral(
                parameters=[k],
                body=k
            )
            cps_expr = cps_transform(expr, identity_k)
            new_exprs.append(cps_expr)

        from fjack.ast import Program
        return Program(expressions=new_exprs)

    def to_ssa(self, cps_program):
        return cps_to_ssa(cps_program)

    def to_jack(self, ssa_program):
        return ssa_to_jack_ast(ssa_program)

def main():
    repl = Repl()
    repl.interact(banner="Welcome to the FJack REPL!", exitmsg="Exiting FJack REPL...")

if __name__ == "__main__":
    main()
