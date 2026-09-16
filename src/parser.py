class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value!r})"


class VariableNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name!r})"


class BinaryNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryNode({self.left!r}, "
            f"{self.operator!r}, {self.right!r})"
        )


class VariableDeclarationNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return (
            f"VariableDeclarationNode("
            f"{self.name!r}, {self.value!r})"
        )


class PrintNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value!r})"


class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return (
            f"IfNode({self.condition!r}, "
            f"{self.body!r}, {self.else_body!r})"
        )


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        nodes = []

        while not self.is_at_end():
            nodes.append(self.parse_statement())

        return nodes

    def parse_statement(self):
        token = self.current()

        if token.type == "BATA":
            return self.parse_variable_declaration()

        if token.type == "LIKHA":
            return self.parse_print()

        if token.type == "AGAR":
            return self.parse_if()

        raise SyntaxError(
            f"Ee command samajh mein na aail: {token.value!r}"
        )

    def parse_variable_declaration(self):
        self.advance()

        name = self.current()

        if name.type != "IDENTIFIER":
            raise SyntaxError(
                "bata ke baad valid variable naam chahi."
            )

        self.advance()

        if self.current().type != "EQUALS":
            raise SyntaxError(
                "Variable declaration mein '=' chahi."
            )

        self.advance()

        value = self.parse_expression()

        return VariableDeclarationNode(
            name.value,
            value
        )

    def parse_print(self):
        self.advance()

        value = self.parse_expression()

        return PrintNode(value)

    def parse_if(self):
        self.advance()

        condition = self.parse_expression()

        if self.current().type != "LIKHA":
            raise SyntaxError(
                "agar ke baad likha command chahi."
            )

        body = self.parse_print()

        else_body = None

        if self.current().type == "NAHI":
            self.advance()

            if self.current().type != "LIKHA":
                raise SyntaxError(
                    "nahi ke baad likha command chahi."
                )

            else_body = self.parse_print()

        return IfNode(
            condition,
            body,
            else_body
        )

    # expression
    # Comparison has lower precedence than arithmetic
    def parse_expression(self):
        return self.parse_comparison()

    # Handles comparison operators
    def parse_comparison(self):
        left = self.parse_addition()

        while self.current().type in (
            "GREATER",
            "LESS",
            "EQUAL_EQUAL",
            "NOT_EQUAL",
            "GREATER_EQUAL",
            "LESS_EQUAL",
        ):
            operator = self.advance()
            right = self.parse_addition()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    # Handles + and -
    def parse_addition(self):
        left = self.parse_multiplication()

        while self.current().type in (
            "PLUS",
            "MINUS"
        ):
            operator = self.advance()
            right = self.parse_multiplication()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    # Handles * and /
    def parse_multiplication(self):
        left = self.parse_primary()

        while self.current().type in (
            "MULTIPLY",
            "DIVIDE"
        ):
            operator = self.advance()
            right = self.parse_primary()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    # Handles numbers, strings and variables
    def parse_primary(self):
        token = self.current()

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(token.value)

        if token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        if token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token.value)

        raise SyntaxError(
            f"Ee value samajh mein na aail: {token.value!r}"
        )

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.tokens[self.position]
        self.position += 1
        return token

    def is_at_end(self):
        return self.current().type == "EOF"
