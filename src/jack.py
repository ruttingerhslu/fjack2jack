import itertools

gensym_counter = itertools.count()

def gensym(prefix="f"):
    return f"{prefix}{next(gensym_counter)}"

def anf_to_jack(anf, vars_declared=None):
    if vars_declared is None:
        vars_declared = set()

    # Binary operations
    if isinstance(anf, list) and anf[0] in ['+', '-', '/', '*', '=']:
        op, e1, e2 = anf
        return f"({anf_to_jack(e1)} {op} {anf_to_jack(e2)})"

    # Atomic values
    if isinstance(anf, (int, float, bool)) or isinstance(anf, str):
        return str(anf)

    # Let binding: ['let', ['x', e1], e2]
    if isinstance(anf, list) and anf[0] == "let":
        _, bindings, body = anf

        code = ""
        for x, e in bindings:
            if x not in vars_declared:
                code += f"var int {x};\n"
                vars_declared.add(x)
            code += f"{x} = {anf_to_jack(e, vars_declared)};\n"

        code += anf_to_jack(body, vars_declared)
        return code

    # If expression
    elif isinstance(anf, list) and anf[0] == "if":
        _, cond, t, e = anf
        return (
            f"if ({anf_to_jack(cond, vars_declared)}) {{\n"
            f"{anf_to_jack(t, vars_declared)}\n"
            f"}} else {{\n"
            f"{anf_to_jack(e, vars_declared)}\n}}"
        )

    # Lambda abstraction
    elif isinstance(anf, list) and anf[0] == "lambda":
        _, params, body = anf
        fname = gensym("f")
        params_str = ", ".join(f"int {p}" for p in params)
        body_code = anf_to_jack(body, set())
        return f"function int {fname}({params_str}) {{\n{body_code}\n}}"

    # Function application
    elif isinstance(anf, list):
        fn, *args = anf
        args_str = ", ".join(anf_to_jack(a, vars_declared) for a in args)
        return f"{fn}({args_str})"

    else:
        raise ValueError(f"Unrecognized ANF form: {anf}")
