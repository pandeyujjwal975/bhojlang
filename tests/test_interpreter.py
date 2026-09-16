import unittest
from unittest.mock import patch, call

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

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertEqual(result, 30)

    def test_subtraction(self):
        interpreter = run_bhojlang(
            """
            bata a = 10
            bata b = 5
            """
        )

        nodes = Parser(
            Lexer("likha a - b").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertEqual(result, 5)

    def test_multiplication(self):
        interpreter = run_bhojlang(
            """
            bata a = 10
            bata b = 5
            """
        )

        nodes = Parser(
            Lexer("likha a * b").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertEqual(result, 50)

    def test_division(self):
        interpreter = run_bhojlang(
            """
            bata a = 10
            bata b = 5
            """
        )

        nodes = Parser(
            Lexer("likha a / b").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertEqual(result, 2.0)

    def test_operator_precedence(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 + 5 * 2").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertEqual(result, 20)

    def test_division_by_zero(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 / 0").tokenize()
        ).parse()

        with self.assertRaises(RuntimeError):
            interpreter.evaluate(
                nodes[0].value
            )

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

    def test_greater_than(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 > 5").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_less_than(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 < 5").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertFalse(result)

    def test_equal_equal(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 == 10").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_not_equal(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 != 5").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_greater_equal(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 >= 10").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_less_equal(self):
        interpreter = run_bhojlang("")

        nodes = Parser(
            Lexer("likha 10 <= 10").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_comparison_with_variables(self):
        interpreter = run_bhojlang(
            """
            bata umar = 20
            """
        )

        nodes = Parser(
            Lexer("likha umar >= 18").tokenize()
        ).parse()

        result = interpreter.evaluate(
            nodes[0].value
        )

        self.assertTrue(result)

    def test_print_comparison(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata umar = 20
                likha umar >= 18
                """
            )

            mock_print.assert_called_once_with(True)

    def test_if_true(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'agar 10 > 5 likha "Adult"'
            )

            mock_print.assert_called_once_with(
                "Adult"
            )

    def test_if_false(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'agar 10 < 5 likha "Adult"'
            )

            mock_print.assert_not_called()

    def test_if_with_variable(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata umar = 20
                agar umar >= 18 likha "Adult"
                """
            )

            mock_print.assert_called_once_with(
                "Adult"
            )

    def test_if_else_true(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'agar 10 > 5 likha "Adult" nahi likha "Minor"'
            )

            mock_print.assert_called_once_with(
                "Adult"
            )

    def test_if_else_false(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'agar 10 < 5 likha "Adult" nahi likha "Minor"'
            )

            mock_print.assert_called_once_with(
                "Minor"
            )

    def test_if_else_with_variable(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata umar = 16
                agar umar >= 18 likha "Adult" nahi likha "Minor"
                """
            )

            mock_print.assert_called_once_with(
                "Minor"
            )

    def test_dohrav(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                'dohrav 3 likha "Ram Ram"'
            )

            self.assertEqual(
                mock_print.call_count,
                3
            )

            mock_print.assert_any_call("Ram Ram")

    def test_dohrav_with_variable(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                bata baar = 2
                dohrav baar likha "BhojLang"
                """
            )

            self.assertEqual(
                mock_print.call_count,
                2
            )

            mock_print.assert_any_call("BhojLang")
    def test_dohrav_block(self):
        with patch("builtins.print") as mock_print:
            run_bhojlang(
                """
                dohrav 3
                    likha "Ram Ram"
                    likha "BhojLang"
                ant
                """
            )

            self.assertEqual(
                mock_print.call_count,
                6
            )

            expected = [
                call("Ram Ram"),
                call("BhojLang"),
                call("Ram Ram"),
                call("BhojLang"),
                call("Ram Ram"),
                call("BhojLang"),
            ]

            mock_print.assert_has_calls(expected)
    
if __name__ == "__main__":
    unittest.main()
