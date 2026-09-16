import unittest
from unittest.mock import patch

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def run_bhojlang(source):
    tokens = Lexer(source).tokenize()
    nodes = Parser(tokens).parse()

    interpreter = Interpreter(nodes)
    interpreter.run()

    return interpreter


class TestInterpreter(unittest.TestCase):

    def test_string_variable(self):
        interpreter = run_bhojlang(
            'bata naam = "Ujjwal"'
        )

        self.assertEqual(
            interpreter.variables["naam"],
            "Ujjwal"
        )

    def test_number_variable(self):
        interpreter = run_bhojlang(
            "bata umar = 20"
        )

        self.assertEqual(
            interpreter.variables["umar"],
            20
        )

    def test_addition(self):
        interpreter = run_bhojlang(
            """
            bata a = 10
            bata b = 20
            """
        )

        nodes = Parser(
            Lexer("likha a + b").tokenize()
        ).parse()

        expression = nodes[0].value
        result = interpreter.evaluate(expression)

        self.assertEqual(result, 30)

    def test_print_string(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'likha "Ram Ram, BhojLang!"'
            )

            mock_print.assert_called_once_with(
                "Ram Ram, BhojLang!"
            )

    def test_print_variable(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata naam = "Ujjwal"
                likha naam
                """
            )

            mock_print.assert_called_once_with(
                "Ujjwal"
            )

    def test_print_addition(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata a = 10
                bata b = 20
                likha a + b
                """
            )

            mock_print.assert_called_once_with(30)

    def test_undefined_variable(self):
        interpreter = Interpreter(
            Parser(
                Lexer("likha naam").tokenize()
            ).parse()
        )

        with self.assertRaises(RuntimeError):
            interpreter.run()


if __name__ == "__main__":
    unittest.main()
