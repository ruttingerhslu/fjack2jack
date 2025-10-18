from fjack.ast import *

def cps_transform(expr: Expression | None) -> Expression:
    """Returns a new AST in Continue-passing Style form."""
    match expr:
        case IntegerLiteral():
            return expr
        case Identifier():
            return expr
        case InfixExpression(left=l, operator=op, right=r):
            return InfixExpression(
                left=cps_transform(l),
                operator=op,
                right=cps_transform(r)
            )
        case FunctionLiteral(parameters=params, body=body):
            new_params = params + [Identifier("k")]
            new_body = FunctionApplication(
                function=Identifier("k"),
                argument=cps_transform(body)
            )
            return FunctionLiteral(parameters=new_params, body=new_body)
        case _:
            raise NotImplementedError(type(expr))
