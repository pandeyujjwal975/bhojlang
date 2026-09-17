from src.parser import (
    NumberNode,
    StringNode,
    BooleanNode,
    VariableNode,
    BinaryNode,
    VariableDeclarationNode,
    AssignmentNode,
    PrintNode,
    LautNode,
    IfNode,
    DohravNode,
    JabtakNode,
    FunctionNode,
    CallNode,
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self, nodes):
        self.nodes = nodes
        self.variables = {}
        self.scopes = [self.variables]
        self.functions = {}

        # Function declarations register karo.
        for node in self.nodes:
            if isinstance(node, FunctionNode):
                self.functions[node.name] = node

    def push_scope(self):
        scope = {}
        self.scopes.append(scope)
        self.variables = scope

    def pop_scope(self):
        if len(self.scopes) <= 1:
            raise RuntimeError("Global scope ke bahar nahi ja sakat bani.")

        self.scopes.pop()
        self.variables = self.scopes[-1]

    def run(self):
        for node in self.nodes:
            self.execute(node)

    def execute(self, node):
        if isinstance(node, FunctionNode):
            return

        if isinstance(node, CallNode):
            if node.name not in self.functions:
                raise RuntimeError(
                    f"Function {node.name!r} define nahi bhail ba."
                )

            function = self.functions[node.name]

            if len(node.arguments) != len(function.parameters):
                raise RuntimeError(
                    f"Function {node.name!r} ke "
                    f"{len(function.parameters)} argument chahi, "
                    f"lekin {len(node.arguments)} milal."
                )

            arguments = [
                self.evaluate(argument)
                for argument in node.arguments
            ]

            self.push_scope()

            for parameter, argument in zip(
                function.parameters,
                arguments
            ):
                self.variables[parameter] = argument

            try:
                for statement in function.body:
                    self.execute(statement)
            except ReturnSignal as signal:
                return signal.value
            finally:
                self.pop_scope()

            return

        if isinstance(node, LautNode):
            raise ReturnSignal(self.evaluate(node.value))

        if isinstance(node, VariableDeclarationNode):
            value = self.evaluate(node.value)
            self.variables[node.name] = value
            return

        if isinstance(node, AssignmentNode):
            if node.name not in self.variables:
                raise RuntimeError(
                    f"Variable {node.name!r} define nahi bhail ba."
                )

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
                if isinstance(node.body, list):
                    for statement in node.body:
                        self.execute(statement)
                else:
                    self.execute(node.body)

            elif node.else_body is not None:
                if isinstance(node.else_body, list):
                    for statement in node.else_body:
                        self.execute(statement)
                else:
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

        if isinstance(node, BooleanNode):
            return node.value

        if isinstance(node, VariableNode):
            if node.name not in self.variables:
                raise RuntimeError(
                    f"Variable {node.name!r} define nahi bhail ba."
                )

            return self.variables[node.name]

        if isinstance(node, CallNode):
            return self.execute(node)

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
