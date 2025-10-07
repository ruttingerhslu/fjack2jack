import code
from typing_extensions import override

from fjack.lexer import Lexer

class Repl(code.InteractiveConsole):
    @override
    def runsource(self, source, filename="<input>", symbol="single"):
        lexer = Lexer(source)
        for token in lexer:
            print(token)

def main():
    repl = Repl()
    repl.interact(banner="Welcome to the FJack REPL!", exitmsg="Exiting FJack REPL...")

if __name__ == "__main__":
    main()
