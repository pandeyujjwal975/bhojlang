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
        return f"VariableDeclarationNode({self.name!r}, {self.value!r})"


class PrintNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value!r})"


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

        return VariableDeclarationNode(name.value, value)

    def parse_print(self):
        self.advance()

        value = self.parse_expression()

        return PrintNode(value)

    def parse_expression(self):
        left = self.parse_primary()

        while self.current().type == "PLUS":
            operator = self.advance()
            right = self.parse_primary()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

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
