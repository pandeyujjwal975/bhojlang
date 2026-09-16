import unittest

from src.lexer import Lexer


class TestLexer(unittest.TestCase):

    def test_keywords(self):
        tokens = Lexer(
            'likha bata agar nahi'
        ).tokenize()

        self.assertEqual(
            [token.type for token in tokens],
            [
                "LIKHA",
                "BATA",
                "AGAR",
                "NAHI",
                "EOF",
            ]
        )

    def test_string(self):
        tokens = Lexer(
            '"Ram Ram, BhojLang!"'
        ).tokenize()

        self.assertEqual(tokens[0].type, "STRING")
        self.assertEqual(
            tokens[0].value,
            "Ram Ram, BhojLang!"
        )

    def test_number(self):
        tokens = Lexer("123").tokenize()

        self.assertEqual(tokens[0].type, "NUMBER")
        self.assertEqual(tokens[0].value, 123)

    def test_identifier(self):
        tokens = Lexer("naam").tokenize()

        self.assertEqual(
            tokens[0].type,
            "IDENTIFIER"
        )
        self.assertEqual(
            tokens[0].value,
            "naam"
        )

    def test_variable_declaration(self):
        tokens = Lexer(
            'bata naam = "Ujjwal"'
        ).tokenize()

        self.assertEqual(
            [token.type for token in tokens],
            [
                "BATA",
                "IDENTIFIER",
                "EQUALS",
                "STRING",
                "EOF",
            ]
        )

    def test_arithmetic_operators(self):
        tokens = Lexer(
            "10 + 5 - 2 * 3 / 2"
        ).tokenize()

        self.assertEqual(
            [token.type for token in tokens],
            [
                "NUMBER",
                "PLUS",
                "NUMBER",
                "MINUS",
                "NUMBER",
                "MULTIPLY",
                "NUMBER",
                "DIVIDE",
                "NUMBER",
                "EOF",
            ]
        )

    def test_comparison_operators(self):
        tokens = Lexer(
            "10 > 5 < 20 == 10 != 7 >= 5 <= 20"
        ).tokenize()

        self.assertEqual(
            [token.type for token in tokens],
            [
                "NUMBER",
                "GREATER",
                "NUMBER",
                "LESS",
                "NUMBER",
                "EQUAL_EQUAL",
                "NUMBER",
                "NOT_EQUAL",
                "NUMBER",
                "GREATER_EQUAL",
                "NUMBER",
                "LESS_EQUAL",
                "NUMBER",
                "EOF",
            ]
        )

    def test_underscore_identifier(self):
        tokens = Lexer("user_name").tokenize()

        self.assertEqual(
            tokens[0].type,
            "IDENTIFIER"
        )
        self.assertEqual(
            tokens[0].value,
            "user_name"
        )

    def test_unknown_character(self):
        with self.assertRaises(SyntaxError):
            Lexer("10 @ 5").tokenize()


if __name__ == "__main__":
    unittest.main()
