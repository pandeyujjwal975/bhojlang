class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value!r})"
        return f"Token({self.type})"


class Lexer:
    KEYWORDS = {
        "likha": "LIKHA",
        "bata": "BATA",
        "agar": "AGAR",
        "nahi": "NAHI",
        "warna": "WARNA",
        "dohrav": "DOHRAV",
        "jabtak": "JABTAK",
        "sach": "SACH",
        "jhooth": "JHOOTH",
        "aur": "AUR",
        "ya": "YA",
        "na": "NA",
        "ant": "ANT",
        "kaam": "KAAM",
        "laut": "LAUT",
    }

    OPERATORS = {
        "=": "EQUALS",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        ">": "GREATER",
        "<": "LESS",
        "==": "EQUAL_EQUAL",
        "!=": "NOT_EQUAL",
        ">=": "GREATER_EQUAL",
        "<=": "LESS_EQUAL",
        "(": "LPAREN",
        ")": "RPAREN",
        ",": "COMMA",
    }

    def __init__(self, text):
        self.text = text
        self.position = 0

    def tokenize(self):
        tokens = []

        while self.position < len(self.text):
            char = self.text[self.position]

            if char == "\n":
                tokens.append(Token("NEWLINE"))
                self.position += 1
                continue

            if char in " \t\r":
                self.position += 1
                continue

            if char == '"':
                tokens.append(self.read_string())
                continue

            if char.isdigit():
                tokens.append(self.read_number())
                continue

            if char.isalpha() or char == "_":
                tokens.append(self.read_word())
                continue

            two_char = self.text[
                self.position:self.position + 2
            ]

            if two_char in self.OPERATORS:
                tokens.append(
                    Token(
                        self.OPERATORS[two_char],
                        two_char
                    )
                )
                self.position += 2
                continue

            if char in self.OPERATORS:
                tokens.append(
                    Token(
                        self.OPERATORS[char],
                        char
                    )
                )
                self.position += 1
                continue

            raise SyntaxError(
                f"Anjaan character: {char!r}"
            )

        tokens.append(Token("EOF"))

        return tokens

    def read_string(self):
        self.position += 1
        start = self.position

        while (
            self.position < len(self.text)
            and self.text[self.position] != '"'
        ):
            self.position += 1

        if self.position >= len(self.text):
            raise SyntaxError(
                "String band na bhail ba."
            )

        value = self.text[start:self.position]

        self.position += 1

        return Token("STRING", value)

    def read_number(self):
        start = self.position

        while (
            self.position < len(self.text)
            and self.text[self.position].isdigit()
        ):
            self.position += 1

        value = self.text[start:self.position]

        return Token(
            "NUMBER",
            int(value)
        )

    def read_word(self):
        start = self.position

        while (
            self.position < len(self.text)
            and (
                self.text[self.position].isalnum()
                or self.text[self.position] == "_"
            )
        ):
            self.position += 1

        word = self.text[start:self.position]

        token_type = self.KEYWORDS.get(
            word,
            "IDENTIFIER"
        )

        return Token(
            token_type,
            word
        )
