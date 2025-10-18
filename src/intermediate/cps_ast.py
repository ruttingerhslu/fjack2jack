from fjack.ast import *

def cps_transform(expr: Expression | None, k: Expression) -> Expression:
    """Returns a new AST in Continue-passing Style form."""
    match expr:
        case IntegerLiteral():
            # F ⟦n⟧ k = k n
            return FunctionApplication(k, expr)
        case Identifier():
            # F ⟦x⟧ k = k x
            return FunctionApplication(k, expr)
        case InfixExpression():
            # F ⟦E1 op E2⟧ k = F ⟦E1⟧ (λv1. F ⟦E2⟧ (λv2. k (v1 op v2)))
            v1 = Identifier("v1")
            v2 = Identifier("v2")
            op_expr = InfixExpression(v1, expr.operator, v2)
            inner = cps_transform(expr.right, FunctionLiteral([v2], FunctionApplication(k, op_expr)))
            return cps_transform(expr.left, FunctionLiteral([v1], inner))
        case FunctionApplication():
            # F ⟦E1 E2⟧ k = F ⟦E1⟧ (λf. F ⟦E2⟧ (λv. f v k))
            f = Identifier("f")
            v = Identifier("v")
            inner_app = FunctionApplication(
                FunctionApplication(Identifier("f"), Identifier("v")),
                k
            )
            arg_cps = cps_transform(expr.argument, FunctionLiteral([v], inner_app))
            return cps_transform(expr.function, FunctionLiteral([f], arg_cps))
        case FunctionLiteral():
            # V ⟦λx. M⟧ = λ(x, k). F ⟦M⟧ k
            new_params = expr.parameters + [Identifier("k")]
            new_body = cps_transform(expr.body, Identifier("k"))
            return FunctionLiteral(new_params, new_body)
        case _:
            raise NotImplementedError(f"Unsupported expression: {expr}")
