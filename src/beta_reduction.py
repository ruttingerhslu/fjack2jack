import copy
import itertools

gensym_counter = itertools.count()

def gensym(prefix="v"):
    return f"{prefix}{next(gensym_counter)}"

def substitute(ast, env):
    if isinstance(ast, str):
        # get value of variable defined in env
        return copy.deepcopy(env.get(ast, ast))

    if not isinstance(ast, list):
        return ast

    if ast[0] == 'lambda':
        params = ast[1]
        body = ast[2]
        # do not substitute inside bound variables
        new_env = {k: v for k, v in env.items() if k not in params}
        return ['lambda', params, substitute(body, new_env)]

    return [substitute(x, env) for x in ast]

# α-renaming for parameters: always freshen
def alpha_rename(params, body):
    body = copy.deepcopy(body)

    new_params = []
    rename_env = {}

    for p in params:
        fresh = gensym(p + "_")
        rename_env[p] = fresh
        new_params.append(fresh)

    # rename parameters in the body
    new_body = substitute(body, rename_env)
    return new_params, new_body

# β-reduction function
def beta_reduce(ast):
    # case: application
    if isinstance(ast, list) and isinstance(ast[0], list):
        func = ast[0]
        args = ast[1:]

        # detect lambda application
        if func[0] == 'lambda':
            params = func[1]
            body = func[2]

            if len(params) == len(args):
                # step 1: α-rename parameters to fresh names
                new_params, new_body = alpha_rename(params, body)

                # step 2: substitute arguments
                env = {new_params[i]: args[i] for i in range(len(params))}
                reduced = substitute(new_body, env)

                return beta_reduce(reduced)

    if isinstance(ast, list):
        return [beta_reduce(x) for x in ast]

    return ast
