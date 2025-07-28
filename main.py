# main.py - punto d'ingresso per compilare file .tal in YAML

import sys
import yaml
from lark import Lark
from compiler import compile_statements

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <file.tal>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()

    parser = Lark.open("grammar.lark", parser="lalr")
    tree = parser.parse(code)

    steps = compile_statements(tree.children)

    # output YAML
    print(yaml.dump({"steps": steps}, sort_keys=False))


if __name__ == "__main__":
    main()
