class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def run(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]

            if token.type == "EOF":
                break

            if token.type == "LIKHA":
                self.position += 1

                if self.position >= len(self.tokens):
                    raise SyntaxError("likha ke baad kuchhu likha nahi ba.")

                value = self.tokens[self.position]

                if value.type != "STRING":
                    raise SyntaxError("likha ke baad text chahi.")

                print(value.value)
                self.position += 1
                continue

            raise SyntaxError(
                f"Ee command samajh mein na aail: {token.value!r}"
            )
