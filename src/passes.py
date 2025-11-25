import itertools

gensym_counter = itertools.count()

def gensym(prefix="f"):
    return f"{prefix}{next(gensym_counter)}"

def lambda_lift(ast, lifted=None):
    """Lift lambdas using their respective let bindings"""
    if lifted is None:
        lifted = []

    if not isinstance(ast, list):
        return ast, lifted

    if len(ast) == 3 and ast[0] == 'let' and isinstance(ast[1], list):
        bindings = ast[1]
        body = ast[2]

        new_bindings = []

        for (name, value) in bindings:
            if (
                isinstance(value, list)
                and len(value) >= 3
                and value[0] == 'lambda'
            ):
                params = value[1]
                lbody = value[2]

                lifted.append(['function', name, params, lbody])

                new_bindings.append([name, name])
            else:
                new_value, lifted = lambda_lift(value, lifted)
                new_bindings.append([name, new_value])

        new_body, lifted = lambda_lift(body, lifted)

        return ['let', new_bindings, new_body], lifted

    new_list = []
    for item in ast:
        new_item, lifted = lambda_lift(item, lifted)
        new_list.append(new_item)

    return new_list, lifted

def flatten_nested_lets(expr):
    """Flatten nested let expressions by removing unnecessary temporary bindings."""
    if not isinstance(expr, list):
        return expr

    if len(expr) == 3 and expr[0] == 'let':
        bindings, body = expr[1], expr[2]
        new_bindings = []
        new_body = flatten_nested_lets(body)

        for var, val in bindings:
            val = flatten_nested_lets(val)
            if isinstance(val, list) and len(val) == 3 and val[0] == 'let':
                inner_bindings, inner_body = val[1], val[2]
                new_bindings.extend(inner_bindings)
                new_body = replace_var(new_body, var, inner_body)
            else:
                new_bindings.append([var, val])

        return ['let', new_bindings, new_body]

    return [flatten_nested_lets(e) for e in expr]

def replace_var(expr, var, val):
    """Recursively replace occurrences of var in expr with val."""
    if isinstance(expr, list):
        return [replace_var(e, var, val) for e in expr]
    elif expr == var:
        return val
    else:
        return expr

def beta_reduction(ast):
    # ((lambda (params) body) arg...)
    if isinstance(ast, list) and isinstance(ast[0], list):
        head = ast[0]
        if (len(head) == 3 and head[0] == 'lambda'):
            params = head[1]
            body = head[2]
            args = ast[1:]

            if len(params) == len(args):
                # construct (let ([p a] ...) body)
                bindings = [[p, beta_reduction(a)] for p, a in zip(params, args)]
                return ['let', bindings, beta_reduction(body)]

    if isinstance(ast, list):
        return [beta_reduction(x) for x in ast]
    return ast
