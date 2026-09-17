import unittest

from src.lexer import Lexer
from src.parser import (
    Parser,
    NumberNode,
    BinaryNode,
    PrintNode,
)


class TestParser(unittest.TestCase):

    def parse(self, source):
        tokens = Lexer(source).tokenize()
        return Parser(tokens).parse()

    def test_greater_than(self):
        nodes = self.parse("likha 10 > 5")

        self.assertIsInstance(nodes[0], PrintNode)
        self.assertIsInstance(nodes[0].value, BinaryNode)

        self.assertEqual(
            nodes[0].value.operator,
            ">"
        )

    def test_less_than(self):
        nodes = self.parse("likha 5 < 10")

        self.assertEqual(
            nodes[0].value.operator,
            "<"
        )

    def test_equal_equal(self):
        nodes = self.parse("likha 10 == 10")

        self.assertEqual(
            nodes[0].value.operator,
            "=="
        )

    def test_not_equal(self):
        nodes = self.parse("likha 10 != 5")

        self.assertEqual(
            nodes[0].value.operator,
            "!="
        )

    def test_greater_equal(self):
        nodes = self.parse("likha 10 >= 10")

        self.assertEqual(
            nodes[0].value.operator,
            ">="
        )

    def test_less_equal(self):
        nodes = self.parse("likha 5 <= 10")

        self.assertEqual(
            nodes[0].value.operator,
            "<="
        )

    def test_comparison_precedence(self):
        nodes = self.parse(
            "likha 10 + 5 > 12"
        )

        comparison = nodes[0].value

        self.assertEqual(
            comparison.operator,
            ">"
        )

        self.assertIsInstance(
            comparison.left,
            BinaryNode
        )

        self.assertEqual(
            comparison.left.operator,
            "+"
        )

        self.assertEqual(
            comparison.left.left.value,
            10
        )

        self.assertEqual(
            comparison.left.right.value,
            5
        )

        self.assertEqual(
            comparison.right.value,
            12
        )
    def test_logical_and(self):
        lexer = Lexer("likha sach aur jhooth")
        tokens = lexer.tokenize()

        nodes = Parser(tokens).parse()

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].value.operator, "aur")

    def test_logical_or(self):
        lexer = Lexer("likha sach ya jhooth")
        tokens = lexer.tokenize()

        nodes = Parser(tokens).parse()

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].value.operator, "ya")

    def test_logical_precedence(self):
        lexer = Lexer("likha sach ya sach aur jhooth")
        tokens = lexer.tokenize()

        nodes = Parser(tokens).parse()

        root = nodes[0].value

        self.assertEqual(root.operator, "ya")
        self.assertEqual(root.right.operator, "aur")


    def test_function_declaration(self):
        lexer = Lexer("""
kaam greet()
    likha "Ram Ram!"
ant
""")
        tokens = lexer.tokenize()
        nodes = Parser(tokens).parse()

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].name, "greet")
        self.assertEqual(len(nodes[0].body), 1)

    def test_function_call(self):
        lexer = Lexer("greet()")
        tokens = lexer.tokenize()
        nodes = Parser(tokens).parse()

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].name, "greet")


if __name__ == "__main__":
    unittest.main()
