
from src.tokens import Token, TokenType


KEYWORDS = {
    "START": TokenType.START,
    "END": TokenType.END,
    "LET": TokenType.LET,
    "SET": TokenType.SET,
    "PRINT": TokenType.PRINT,
    "INPUT": TokenType.INPUT,
    "IF": TokenType.IF,
    "ELSE": TokenType.ELSE,
    "THEN": TokenType.THEN,
    "WHILE": TokenType.WHILE,
    "DO": TokenType.DO,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def current_char(self):
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def peek(self):
        next_position = self.position + 1

        if next_position >= len(self.source):
            return None

        return self.source[next_position]

    def advance(self):
        char = self.current_char()

        if char is not None:
            self.position += 1

            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1

        return char

    def add_token(self, token_type, value):
        self.tokens.append(
            Token(token_type, value, self.line, self.column)
        )

    def skip_comment(self):
        while self.current_char() not in (None, "\n"):
            self.advance()

    def read_number(self):
        start = self.position
        has_decimal = False

        while (char := self.current_char()) is not None:
            if char.isdigit():
                self.advance()
            elif char == "." and not has_decimal:
                has_decimal = True
                self.advance()
            else:
                break

        value = self.source[start:self.position]

        if value.endswith("."):
            raise SyntaxError(
                f"Invalid number '{value}' at line {self.line}"
            )

        return float(value) if has_decimal else int(value)

    def read_identifier(self):
        start = self.position

        while (char := self.current_char()) is not None:
            if char.isalnum() or char == "_":
                self.advance()
            else:
                break

        return self.source[start:self.position]

    def read_string(self):
        self.advance()  # Skip opening quote
        start = self.position

        while (char := self.current_char()) is not None:
            if char == '"':
                value = self.source[start:self.position]
                self.advance()
                return value

            if char == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {self.line}"
                )

            self.advance()

        raise SyntaxError(
            f"Unterminated string at line {self.line}"
        )

    def tokenize(self):
        while (char := self.current_char()) is not None:

            if char in " \t\r":
                self.advance()
                continue

            if char == "\n":
                self.add_token(TokenType.NEWLINE, "\\n")
                self.advance()
                continue

            if char == "#":
                self.skip_comment()
                continue

            if char.isdigit():
                value = self.read_number()
                self.add_token(TokenType.NUMBER, value)
                continue

            if char.isalpha() or char == "_":
                value = self.read_identifier()
                token_type = KEYWORDS.get(
                    value, TokenType.IDENTIFIER
                )
                self.add_token(token_type, value)
                continue

            if char == '"':
                value = self.read_string()
                self.add_token(TokenType.STRING, value)
                continue

            two_char_operators = {
                "==": TokenType.EQUAL,
                "!=": TokenType.NOT_EQUAL,
                ">=": TokenType.GREATER_EQUAL,
                "<=": TokenType.LESS_EQUAL,
            }

            two_char = char + (self.peek() or "")

            if two_char in two_char_operators:
                self.advance()
                self.advance()
                self.add_token(two_char_operators[two_char], two_char)
                continue

            single_char_operators = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "%": TokenType.MODULO,
                "=": TokenType.ASSIGN,
                ">": TokenType.GREATER,
                "<": TokenType.LESS,
                "(": TokenType.LEFT_PAREN,
                ")": TokenType.RIGHT_PAREN,
            }

            if char in single_char_operators:
                self.advance()
                self.add_token(single_char_operators[char], char)
                continue

            raise SyntaxError(
                f"Unexpected character '{char}' "
                f"at line {self.line}, column {self.column}"
            )

        self.tokens.append(
            Token(TokenType.EOF, None, self.line, self.column)
        )

        return self.tokens
