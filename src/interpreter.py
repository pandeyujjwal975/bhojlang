from src.parser import (
    NumberNode,
    StringNode,
    VariableNode,
    BinaryNode,
    VariableDeclarationNode,
    PrintNode,
    IfNode,
    DohravNode,
    JabtakNode,
)


class Interpreter:
    def __init__(self, nodes):
        self.nodes = nodes
        self.variables = {}

    def run(self):
        for node in self.nodes:
            self.execute(node)

    def execute(self, node):
        if isinstance(node, VariableDeclarationNode):
            value = self.evaluate(node.value)
            self.variables[node.name] = value
            return

        if isinstance(node, PrintNode):
            value = self.evaluate(node.value)
            print(value)
            return

        if isinstance(node, IfNode):
            condition = self.evaluate(node.condition)

            if condition:
                self.execute(node.body)

            elif node.else_body is not None:
                self.execute(node.else_body)

            return

        if isinstance(node, DohravNode):
            count = self.evaluate(node.count)

            if not isinstance(count, int):
                raise RuntimeError(
                    "dohrav ke liye count integer hona chahi."
                )

            if count < 0:
                raise RuntimeError(
                    "dohrav ke liye count negative nahi ho sakta."
                )

            for _ in range(count):
                for statement in node.body:
                    self.execute(statement)

            return

        if isinstance(node, JabtakNode):
            while self.evaluate(node.condition):
                for statement in node.body:
                    self.execute(statement)

            return

        raise RuntimeError(
            f"Ee AST node samajh mein na aail: "
            f"{type(node).__name__}"
        )

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, VariableNode):
            if node.name not in self.variables:
                raise RuntimeError(
                    f"Variable {node.name!r} define nahi bhail ba."
                )

            return self.variables[node.name]

        if isinstance(node, BinaryNode):
            return self.evaluate_binary(node)

        raise RuntimeError(
            f"Ee expression samajh mein na aail: "
            f"{type(node).__name__}"
        )

    def evaluate_binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == ">":
            return left > right

        if node.operator == "<":
            return left < right

        if node.operator == "==":
            return left == right

        if node.operator == "!=":
            return left != right

        if node.operator == ">=":
            return left >= right

        if node.operator == "<=":
            return left <= right

        if not isinstance(left, (int, float)):
            raise RuntimeError(
                "Arithmetic mein pahila value number chahi."
            )

        if not isinstance(right, (int, float)):
            raise RuntimeError(
                "Arithmetic mein dusra value number chahi."
            )

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            if right == 0:
                raise RuntimeError(
                    "Zero se divide nahi kar sakat bani."
                )

            return left / right

        raise RuntimeError(
            f"Ee operator abhi supported nahi ba: "
            f"{node.operator!r}"
        )
