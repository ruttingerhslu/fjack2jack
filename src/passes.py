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


def flatten(expr):
    """
    Flatten nested `let` expressions into a linear sequence of bindings.
    Input is assumed to already be in ANF form.
    Output: (bindings, value)
    """
    if not isinstance(expr, list):
        return [], expr
    elif expr[0] == 'let':
        bindings, body = expr[1], expr[2]
        acc = []
        for var, val in bindings:
            bnds_v, val_v = flatten(val)
            acc.extend(bnds_v)
            acc.append([var, val_v])
        bnds_body, body_val = flatten(body)
        acc.extend(bnds_body)
        return acc, body_val
    elif isinstance(expr, list):
        subexprs = expr[1:]
        acc = []
        flat_subs = []
        for e in subexprs:
            bnds_e, val_e = flatten(e)
            acc.extend(bnds_e)
            flat_subs.append(val_e)
        return acc, [expr[0]] + flat_subs

def flatten_program(expr):
    bindings, value = flatten(expr)
    return ['let', bindings, value]
