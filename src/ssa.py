phi_assignments: dict[str, dict[str, list[str]]] = {}

def collect_phi_assignments(expr):
    """Collect all jump labels and their bound variables."""
    if not isinstance(expr, list) or not expr:
        return

    if expr[0] == 'letrec':
        _, bindings, body = expr
        for name, lam in bindings:
            if isinstance(lam, list) and lam[0] == 'lambda_jump':
                _, params, _ = lam
                phi_assignments[name] = {x: [] for x in params}
        collect_phi_assignments(body)

    for e in expr[1:]:
        collect_phi_assignments(e)

def exp(e):
    """Transform CPS expression to SSA expression"""
    # transform binary op expression
    if isinstance(e, list) and len(e) == 3 and e[0] in ['+', '-', '*', '/', '>', '<', '=']:
        return [exp(e[1]), e[0], exp(e[2])]
    return e

def g(m):
    """G: M' -> B"""
    # G([(let ((x E)) M')]) = x <- E; G([M'])
    if m[0] == 'let':
        _, bindings, body = m
        (x, e), = bindings
        return [x, '<-', e, ';', g(body)]
    # G([(j E_0,i E_1,i ...)]) = goto j_i;
    elif isinstance(m[0], str) and m[0] in phi_assignments:
        label = m[0]
        args = m[1:]
        for var, val in zip(phi_assignments[label].keys(), args):
            phi_assignments[label][var].append(val)
        l_index = len(phi_assignments[label]['x'])
        return ['goto', f'{label}_{l_index};']
    # G([(if E M_1' M_2')]) = if E then G([M_1']) else G([M_2'])
    elif m[0] == 'if':
        _, cond, then_m, else_m = m
        return ['if', cond, 'then', g(then_m), 'else', g(else_m)]
    # G([(letrec (...) M')]) = G([M'])
    elif m[0] == 'letrec':
        _, bindings, body = m
        return g(body)
    # G([(k E)]) = return E;
    elif m[0] == 'k' and len(m) == 2:
        return ['return', exp(m[1]), ';']
    # G([(E...k)]) = return E(...);
    elif m[-1] == 'k':
        func = m[0]
        args = m[1:-1]
        return ['return', exp(func), [args], ';']

    return m

def g_proc(p):
    """G_proc([(λ_proc (x ...) M')]) = proc(x ... k) { G([M']) G_jump([(lamda_jump ...)]) ... }"""
    if not (isinstance(p, list) and p[0] == 'lambda_proc'):
         return p
    _, params, body = p

    # remove continuation argument if present
    if params and params[-1] == 'k':
        params = params[:-1]

    m = g(body)

    jump_blocks = []
    if isinstance(body, list) and body[0] == 'letrec':
        _, bindings, _ = body
        for (label, lam) in bindings:
            if lam[0] == 'lambda_jump':
                jump_blocks.append(g_jump(label, lam))

    return ['proc', params, m, *jump_blocks]

def g_jump(j, m):
    """G_jump: (λ_jump (x...) M') → j: x <- φ(...); ...; G(M')"""
    if not (isinstance(m, list) and m and m[0] == 'lambda_jump'):
        return m
    _, [*_], body = m
    return [j, ':', phi_assignments[j], g(body)]
