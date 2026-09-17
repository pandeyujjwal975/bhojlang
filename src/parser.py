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


class BooleanNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanNode({self.value})"


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
            f"BinaryNode("
            f"{self.left!r}, "
            f"{self.operator!r}, "
            f"{self.right!r})"
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


class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return (
            f"AssignmentNode("
            f"{self.name!r}, {self.value!r})"
        )


class PrintNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value!r})"


class LautNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"LautNode({self.value!r})"


class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return (
            f"IfNode("
            f"{self.condition!r}, "
            f"{self.body!r}, "
            f"{self.else_body!r})"
        )


class DohravNode:
    def __init__(self, count, body):
        self.count = count
        self.body = body

    def __repr__(self):
        return f"DohravNode({self.count!r}, {self.body!r})"


class JabtakNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"JabtakNode({self.condition!r}, {self.body!r})"


class FunctionNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return (
            f"FunctionNode("
            f"{self.name!r}, "
            f"{self.parameters!r}, "
            f"{self.body!r}"
            f")"
        )


class CallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return (
            f"CallNode("
            f"{self.name!r}, "
            f"{self.arguments!r}"
            f")"
        )


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()

        if self.position < len(self.tokens) - 1:
            self.position += 1

        return token

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise SyntaxError(
                f"Umeed {token_type} rahal, "
                f"lekin {token.type} milal."
            )

        self.advance()
        return token

    def skip_newlines(self):
        while self.current().type == "NEWLINE":
            self.advance()

    def parse(self):
        nodes = []

        self.skip_newlines()

        while self.current().type != "EOF":
            nodes.append(self.parse_statement())
            self.skip_newlines()

        return nodes

    def parse_statement(self):
        token = self.current()

        if token.type == "BATA":
            return self.parse_variable_declaration()

        if token.type == "LIKHA":
            return self.parse_print()

        if token.type == "AGAR":
            return self.parse_if()

        if token.type == "DOHRAV":
            return self.parse_dohrav()

        if token.type == "JABTAK":
            return self.parse_jabtak()

        if token.type == "KAAM":
            return self.parse_function()

        if token.type == "LAUT":
            return self.parse_laut()

        if token.type == "IDENTIFIER":
            if (
                self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1].type == "LPAREN"
            ):
                return self.parse_call()

            return self.parse_assignment()

        raise SyntaxError(
            f"Anjaan statement: {token.type}"
        )

    def parse_laut(self):
        self.expect("LAUT")
        value = self.parse_expression()
        return LautNode(value)

    def parse_variable_declaration(self):
        self.expect("BATA")

        name = self.expect("IDENTIFIER").value

        self.expect("EQUALS")

        value = self.parse_expression()

        return VariableDeclarationNode(
            name,
            value
        )

    def parse_assignment(self):
        name = self.expect("IDENTIFIER").value

        self.expect("EQUALS")

        value = self.parse_expression()

        return AssignmentNode(
            name,
            value
        )

    def parse_print(self):
        self.expect("LIKHA")

        value = self.parse_expression()

        return PrintNode(value)

    def parse_if(self):
        self.expect("AGAR")

        condition = self.parse_expression()

        self.expect("LIKHA")

        body = PrintNode(
            self.parse_expression()
        )

        else_body = None

        if self.current().type == "NAHI":
            self.advance()

            self.expect("LIKHA")

            else_body = PrintNode(
                self.parse_expression()
            )

        return IfNode(
            condition,
            body,
            else_body
        )

    def parse_dohrav(self):
        self.expect("DOHRAV")

        count = self.parse_expression()

        # Single-line loop:
        # dohrav 3 likha "Ram Ram"
        if self.current().type == "LIKHA":
            body = self.parse_statement()

            return DohravNode(
                count,
                [body]
            )

        # Block loop:
        # dohrav 3
        #     likha "Ram Ram"
        # ant

        self.skip_newlines()

        body = []

        while self.current().type != "ANT":
            if self.current().type == "EOF":
                raise SyntaxError(
                    "dohrav ke block ke ant mein 'ant' chahi."
                )

            body.append(self.parse_statement())
            self.skip_newlines()

        self.expect("ANT")

        return DohravNode(
            count,
            body
        )

    def parse_jabtak(self):
        self.expect("JABTAK")

        condition = self.parse_expression()

        self.skip_newlines()

        body = []

        while self.current().type != "ANT":
            body.append(self.parse_statement())
            self.skip_newlines()

        self.expect("ANT")

        return JabtakNode(
            condition,
            body
        )

    def parse_function(self):
        self.expect("KAAM")

        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        parameters = []

        if self.current().type != "RPAREN":
            while True:
                parameters.append(
                    self.expect("IDENTIFIER").value
                )

                if self.current().type != "COMMA":
                    break

                self.advance()

        self.expect("RPAREN")

        self.skip_newlines()

        body = []

        while self.current().type != "ANT":
            if self.current().type == "EOF":
                raise SyntaxError(
                    "kaam ke block ke ant mein 'ant' chahi."
                )

            body.append(self.parse_statement())
            self.skip_newlines()

        self.expect("ANT")

        return FunctionNode(
            name,
            parameters,
            body
        )

    def parse_call(self):
        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        arguments = []

        if self.current().type != "RPAREN":
            while True:
                arguments.append(
                    self.parse_expression()
                )

                if self.current().type != "COMMA":
                    break

                self.advance()

        self.expect("RPAREN")

        return CallNode(
            name,
            arguments
        )

    def parse_expression(self):
        return self.parse_ya()

    def parse_ya(self):
        left = self.parse_aur()

        while self.current().type == "YA":
            operator = self.advance()
            right = self.parse_aur()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    def parse_aur(self):
        left = self.parse_comparison()

        while self.current().type == "AUR":
            operator = self.advance()
            right = self.parse_comparison()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    def parse_comparison(self):
        left = self.parse_addition()

        while self.current().type in {
            "GREATER",
            "LESS",
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "EQUAL_EQUAL",
            "NOT_EQUAL",
        }:
            operator = self.advance()
            right = self.parse_addition()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    def parse_addition(self):
        left = self.parse_multiplication()

        while self.current().type in {
            "PLUS",
            "MINUS",
        }:
            operator = self.advance()
            right = self.parse_multiplication()

            left = BinaryNode(
                left,
                operator.value,
                right
            )

        return left

    def parse_multiplication(self):
        left = self.parse_primary()

        while self.current().type in {
            "MULTIPLY",
            "DIVIDE",
        }:
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

        if token.type == "SACH":
            self.advance()
            return BooleanNode(True)

        if token.type == "JHOOTH":
            self.advance()
            return BooleanNode(False)

        if token.type == "IDENTIFIER":
            self.advance()

            if self.current().type == "LPAREN":
                self.advance()

                arguments = []

                if self.current().type != "RPAREN":
                    arguments.append(self.parse_expression())

                    while self.current().type == "COMMA":
                        self.advance()
                        arguments.append(self.parse_expression())

                self.expect("RPAREN")

                return CallNode(token.value, arguments)

            return VariableNode(token.value)

        raise SyntaxError(
            f"Anjaan expression: {token.type}"
        )
