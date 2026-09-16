class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.variables = {}

    def run(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]

            if token.type == "EOF":
                break

            if token.type == "BATA":
                self.handle_variable()
                continue

            if token.type == "LIKHA":
                self.handle_print()
                continue

            raise SyntaxError(
                f"Ee command samajh mein na aail: {token.value!r}"
            )

    def handle_variable(self):
        # bata ke baad variable name
        self.position += 1

        if self.position >= len(self.tokens):
            raise SyntaxError("bata ke baad variable ke naam chahi.")

        name = self.tokens[self.position]

        if name.type != "IDENTIFIER":
            raise SyntaxError("bata ke baad valid variable naam chahi.")

        # =
        self.position += 1

        if self.position >= len(self.tokens):
            raise SyntaxError("Variable ke value missing ba.")

        equals = self.tokens[self.position]

        if equals.type != "EQUALS":
            raise SyntaxError("Variable declaration mein '=' chahi.")

        # value
        self.position += 1

        if self.position >= len(self.tokens):
            raise SyntaxError("Variable ke value missing ba.")

        value = self.get_value()

        self.variables[name.value] = value

    def handle_print(self):
        # likha ke baad value/expression
        self.position += 1

        if self.position >= len(self.tokens):
            raise SyntaxError("likha ke baad kuchhu likha chahi.")

        value = self.get_value()

        # Addition
        if self.position < len(self.tokens):
            operator = self.tokens[self.position]

            if operator.type == "PLUS":
                self.position += 1

                right = self.get_value()

                if not isinstance(value, (int, float)):
                    raise SyntaxError("Addition sirf number ke saath ho sakta hai.")

                if not isinstance(right, (int, float)):
                    raise SyntaxError("Addition sirf number ke saath ho sakta hai.")

                value = value + right

        print(value)

    def get_value(self):
        token = self.tokens[self.position]

        if token.type == "STRING":
            self.position += 1
            return token.value

        if token.type == "NUMBER":
            self.position += 1
            return token.value

        if token.type == "IDENTIFIER":
            self.position += 1

            if token.value not in self.variables:
                raise SyntaxError(
                    f"Variable {token.value!r} define nahi bhail ba."
                )

            return self.variables[token.value]

        raise SyntaxError(
            f"Ee value samajh mein na aail: {token.value!r}"
        )
