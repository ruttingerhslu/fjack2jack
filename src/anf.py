import itertools

gensym_counter = itertools.count()

def gensym(prefix="t"):
    return f"{prefix}{next(gensym_counter)}"

def normalize_term(m):
    return normalize(m, lambda x: x)

def is_value(expr):
    return (
        isinstance(expr, (int, float, bool, str))
        or expr in ['+', '-', '*', '/', '=']
        or (isinstance(expr, list) and expr and expr[0] == 'lambda')
    )

def normalize_name(m, k):
    def cont(n):
        if is_value(n):
            return k(n)
        else:
            t = gensym()
            return ['let', [t, n], k(t)]
    return normalize(m, cont)

def normalize_name_star(exprs, k):
    if not exprs:
        return k([])
    first, *rest = exprs
    return normalize_name(first, lambda t:
        normalize_name_star(rest, lambda t_star:
            k([t] + t_star)))

def normalize(m, k):
    # lambda abstractions
    if isinstance(m, list) and len(m) >= 3 and m[0] == 'lambda':
        params, body = m[1], m[2]
        return k(['lambda', params, normalize_term(body)])

    # let bindings
    elif isinstance(m, list) and len(m) == 3 and m[0] == 'let' and isinstance(m[1], list):
        bindings = m[1]
        m2 = m[2]

        def process_bindings(bindings, k):
            if not bindings:
                return k([])
            (x, m1), *rest = bindings
            return normalize(m1, lambda n1:
                process_bindings(rest, lambda ns: k([[x, n1]] + ns))
            )

        return process_bindings(bindings, lambda normalized_bindings:
            ['let', normalized_bindings, normalize(m2, k)]
        )

    # if expression
    elif isinstance(m, list) and len(m) == 4 and m[0] == 'if':
        m1, m2, m3 = m[1], m[2], m[3]
        return normalize_name(m1, lambda t: k(['if', t, normalize_term(m2), normalize_term(m3)]))

    # function application or primitive op
    elif isinstance(m, list) and len(m) >= 1:
        fn, *args = m
        return normalize_name(fn, lambda t: normalize_name_star(args, lambda t_star: k([t] + t_star)))

    # atomic value
    elif is_value(m):
        return k(m)

    else:
        raise ValueError(f"unrecognized form: {m}")
