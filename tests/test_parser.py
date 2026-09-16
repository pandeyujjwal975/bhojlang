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


if __name__ == "__main__":
    unittest.main()
