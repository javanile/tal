# compiler.py - traduce AST in struttura dati (dict) da serializzare YAML

from lark.tree import Tree

def compile_statements(statements):
    """
    Compila lista di statement (AST) in struttura dati
    """
    steps = []
    step_counter = 0

    def compile_stmt(stmt):
        nonlocal step_counter

        if stmt.data == "func_stmt":
            func_name = stmt.children[0].children[0].value
            args = [extract_arg(a) for a in stmt.children[0].children[1].children] if len(stmt.children[0].children) > 1 else []
            step_id = f"step_{step_counter}"
            step_counter += 1
            return {
                "id": step_id,
                "name": func_name,
                "args": args,
                "type": "function"
            }
        elif stmt.data == "block_stmt":
            # blocco di statement, ricorsivo
            block_steps = []
            for s in stmt.children:
                block_steps.append(compile_stmt(s))
            return {
                "type": "block",
                "steps": block_steps
            }
        else:
            raise ValueError(f"Unknown statement {stmt.data}")

    def extract_arg(arg):
        if isinstance(arg, Tree):
            if arg.data == "function_call":
                func_name = arg.children[0].value
                args = [extract_arg(a) for a in arg.children[1].children] if len(arg.children) > 1 else []
                return {"func": func_name, "args": args}
            elif arg.data == "block_stmt":
                return compile_stmt(arg)
            else:
                return str(arg)
        else:
            return str(arg)

    for stmt in statements:
        compiled = compile_stmt(stmt)
        steps.append(compiled)

    return steps