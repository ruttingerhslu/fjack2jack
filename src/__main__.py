import code
from typing_extensions import override

from .fjack.lexer import Lexer
from .fjack.parser import Parser

from .intermediate.cps import CPS
from .intermediate.ssa import SSA

class Repl(code.InteractiveConsole):
    @override
    def runsource(self, source: str, filename: str="<input>", symbol: str="single"):
        lexer = Lexer(source)
        p = Parser(lexer)

        program = p.parse_program()

        cps = CPS()
        cps_ast = cps.transform_v(program)
        print(cps_ast)

        return True

def main():
    repl = Repl()
    repl.interact(banner="Welcome to the FJack REPL!", exitmsg="Exiting FJack REPL...")

if __name__ == "__main__":
    main()
