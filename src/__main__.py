from .anf import normalize_term
from .beta_reduction import beta_reduce
from .lambda_lifting import lambda_lift
from .jack import JackGenerator
from .fjack import *

def main(prompt: str = "fjack.py> "):
    """A prompt read-eval-print loop."""
    while True:
        fjack_code = input(prompt)
        ast = parse(fjack_code)

        ast = beta_reduce(ast)
        print("Pass: beta_reduce")
        print(ast)
        ast = normalize_term(ast)
        print("Pass: a-normalization")
        print(ast)
        ast, lifted = lambda_lift(ast)
        print("Pass: lambda lifting")
        print(ast)

        gen = JackGenerator()
        jack_code = gen.generate_jack(ast, lifted)
        print(jack_code)

if __name__ == "__main__":
    main()
