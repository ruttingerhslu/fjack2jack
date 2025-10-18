from typing import Callable

from .ssa_ast import *
from fjack.ast import *

def cps_to_ssa(
    expr: Expression | None,
    temp_gen: Callable[[], str] | None = None,
    label_gen: Callable[[], str] | None = None
) -> tuple[list[SSAStatement | SSAProcedure], str]:
    """
    Convert a CPS expression into SSA form.
    Returns: list of SSAStatement | SSAProcedure, and final variable name.
    """
    if temp_gen is None:
        temp_counter = 0

        def temp_gen_func():
            nonlocal temp_counter
            name = f"t{temp_counter}"
            temp_counter += 1
            return name

        temp_gen = temp_gen_func

    if label_gen is None:
        label_counter = 0

        def label_gen_func():
            nonlocal label_counter
            name = f"L{label_counter}"
            label_counter += 1
            return name

        label_gen = label_gen_func

    match expr:
        case IntegerLiteral():
            var = temp_gen()
            return [SSAStatement(var, str(expr.value))], var

        case Identifier():
            return [], expr.value

        case InfixExpression():
            left_stmts, left_var = cps_to_ssa(expr.left, temp_gen, label_gen)
            right_stmts, right_var = cps_to_ssa(expr.right, temp_gen, label_gen)
            var = temp_gen()
            stmt = SSAStatement(var, f"{left_var} {expr.operator} {right_var}")
            return left_stmts + right_stmts + [stmt], var

        case FunctionApplication():
            func_stmts, func_var = cps_to_ssa(expr.function, temp_gen, label_gen)
            arg_stmts, arg_var = cps_to_ssa(expr.argument, temp_gen, label_gen)
            call_var = temp_gen()
            stmt = SSAStatement(call_var, f"{func_var}({arg_var})")
            return func_stmts + arg_stmts + [stmt], call_var

        case FunctionLiteral():
            body_items, ret_var = cps_to_ssa(expr.body, temp_gen, label_gen)

            # Separate statements and nested procedures
            body_stmts: list[SSAStatement] = [s for s in body_items if isinstance(s, SSAStatement)]
            nested_procs: list[SSAProcedure] = [p for p in body_items if isinstance(p, SSAProcedure)]

            proc_name = label_gen()
            proc = SSAProcedure(
                proc_name,
                [p.value for p in expr.parameters],
                body_stmts + [SSAStatement("return", ret_var)],
            )

            proc_var = temp_gen()
            combined: list[SSAStatement | SSAProcedure] = [*nested_procs, proc]
            return combined, proc_var

        case _:
            raise NotImplementedError(f"SSA conversion not implemented for {expr}")
