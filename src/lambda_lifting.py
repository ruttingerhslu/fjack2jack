def lambda_lift(ast, lifted=None):
    """Lift lambdas using their respective let bindings"""
    if lifted is None:
        lifted = []

    elif not isinstance(ast, list):
        return ast, lifted

    elif len(ast) == 3 and ast[0] == 'let' and isinstance(ast[1], list):
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
