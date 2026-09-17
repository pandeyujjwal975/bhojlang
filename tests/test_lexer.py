import unittest

from src.lexer import Lexer


class TestLexer(unittest.TestCase):

    def test_keywords(self):
        lexer = Lexer("likha bata agar nahi dohrav jabtak ant")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "LIKHA")
        self.assertEqual(tokens[1].type, "BATA")
        self.assertEqual(tokens[2].type, "AGAR")
        self.assertEqual(tokens[3].type, "NAHI")
        self.assertEqual(tokens[4].type, "DOHRAV")
        self.assertEqual(tokens[5].type, "JABTAK")
        self.assertEqual(tokens[6].type, "ANT")

    def test_number(self):
        lexer = Lexer("123")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "NUMBER")
        self.assertEqual(tokens[0].value, 123)

    def test_string(self):
        lexer = Lexer('"hello"')
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "STRING")
        self.assertEqual(tokens[0].value, "hello")

    def test_identifier(self):
        lexer = Lexer("naam")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "IDENTIFIER")
        self.assertEqual(tokens[0].value, "naam")

    def test_underscore_identifier(self):
        lexer = Lexer("user_name")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "IDENTIFIER")
        self.assertEqual(tokens[0].value, "user_name")

    def test_variable_declaration(self):
        lexer = Lexer("bata naam = 10")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "BATA")
        self.assertEqual(tokens[1].type, "IDENTIFIER")
        self.assertEqual(tokens[1].value, "naam")
        self.assertEqual(tokens[2].type, "EQUALS")
        self.assertEqual(tokens[3].type, "NUMBER")
        self.assertEqual(tokens[3].value, 10)

    def test_arithmetic_operators(self):
        lexer = Lexer("10 + 5 - 2 * 3 / 2")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[1].type, "PLUS")
        self.assertEqual(tokens[3].type, "MINUS")
        self.assertEqual(tokens[5].type, "MULTIPLY")
        self.assertEqual(tokens[7].type, "DIVIDE")

    def test_comparison_operators(self):
        lexer = Lexer("> < >= <= == !=")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "GREATER")
        self.assertEqual(tokens[1].type, "LESS")
        self.assertEqual(tokens[2].type, "GREATER_EQUAL")
        self.assertEqual(tokens[3].type, "LESS_EQUAL")
        self.assertEqual(tokens[4].type, "EQUAL_EQUAL")
        self.assertEqual(tokens[5].type, "NOT_EQUAL")

    def test_unknown_character(self):
        with self.assertRaises(SyntaxError):
            Lexer("10 @ 5").tokenize()

    def test_logical_keywords(self):
        lexer = Lexer("sach jhooth aur ya na")
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, "SACH")
        self.assertEqual(tokens[1].type, "JHOOTH")
        self.assertEqual(tokens[2].type, "AUR")
        self.assertEqual(tokens[3].type, "YA")
        self.assertEqual(tokens[4].type, "NA")
        self.assertEqual(tokens[5].type, "EOF")


if __name__ == "__main__":
    unittest.main()
