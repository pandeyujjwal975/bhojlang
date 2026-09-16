import sys

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def main():
    if len(sys.argv) != 2:
        print("Istemaal: python bhojlang.py <file.bhoj>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        nodes = parser.parse()

        interpreter = Interpreter(nodes)
        interpreter.run()

    except FileNotFoundError:
        print(f"File na mili: {filename}")
        sys.exit(1)

    except (SyntaxError, RuntimeError) as error:
        print(f"BhojLang error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
