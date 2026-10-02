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
    ListNode,
    IndexNode,
    IndexAssignmentNode,
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
        self.builtins = {
            "lambai": self.builtin_lambai,
            "jodo": self.builtin_jodo,
            "nikalo": self.builtin_nikalo,
        }

        # Function declarations register karo.
        for node in self.nodes:
            if isinstance(node, FunctionNode):
                self.functions[node.name] = node

    def builtin_lambai(self, arguments):
        if len(arguments) != 1:
            raise RuntimeError(
                f"Function 'lambai' ke 1 argument chahi, "
                f"lekin {len(arguments)} milal."
            )

        value = arguments[0]

        if not isinstance(value, (list, str)):
            raise RuntimeError(
                "lambai ke argument list ya string hona chahi."
            )

        return len(value)

    def builtin_jodo(self, arguments):
        if len(arguments) != 2:
            raise RuntimeError(
                f"Function 'jodo' ke 2 argument chahi, "
                f"lekin {len(arguments)} milal."
            )

        collection = arguments[0]
        value = arguments[1]

        if not isinstance(collection, list):
            raise RuntimeError(
                "jodo ke pahila argument list hona chahi."
            )

        collection.append(value)
        return

    def builtin_nikalo(self, arguments):
        if len(arguments) != 1:
            raise RuntimeError(
                f"Function 'nikalo' ke 1 argument chahi, "
                f"lekin {len(arguments)} milal."
            )

        collection = arguments[0]

        if not isinstance(collection, list):
            raise RuntimeError(
                "nikalo ke argument list hona chahi."
            )

        if not collection:
            raise RuntimeError(
                "Khali list se nikalo nahi kar sakat bani."
            )

        return collection.pop()

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
            if node.name in self.builtins:
                arguments = [
                    self.evaluate(argument)
                    for argument in node.arguments
                ]
                return self.builtins[node.name](arguments)

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

        if isinstance(node, IndexAssignmentNode):
            collection = self.evaluate(node.target.collection)
            index = self.evaluate(node.target.index)
            value = self.evaluate(node.value)

            if not isinstance(index, int):
                raise RuntimeError(
                    "List index integer hona chahi."
                )

            if not isinstance(collection, list):
                raise RuntimeError(
                    "Index assignment sirf list par use kar sakat bani."
                )

            if index < 0 or index >= len(collection):
                raise RuntimeError(
                    f"List index {index} range se bahar ba."
                )

            collection[index] = value
            return

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

        if isinstance(node, ListNode):
            return [
                self.evaluate(element)
                for element in node.elements
            ]

        if isinstance(node, IndexNode):
            collection = self.evaluate(node.collection)
            index = self.evaluate(node.index)

            if not isinstance(index, int):
                raise RuntimeError(
                    "List index integer hona chahi."
                )

            if not isinstance(collection, list):
                raise RuntimeError(
                    "Index sirf list par use kar sakat bani."
                )

            if index < 0 or index >= len(collection):
                raise RuntimeError(
                    f"List index {index} range se bahar ba."
                )

            return collection[index]

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
        # Logical NOT
        if node.operator == "na":
            return not bool(self.evaluate(node.right))

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
        if node.operator == "aur":
            return bool(left) and bool(right)

        if node.operator == "ya":
            return bool(left) or bool(right)


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
