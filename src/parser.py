
from src.tokens import TokenType
from src.ast_nodes import (
    Program,
    LetStatement,
    SetStatement,
    PrintStatement,
    InputStatement,
    IfStatement,
    WhileStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current_token()

        if token.type != TokenType.EOF:
            self.position += 1

        return token

    def check(self, token_type):
        return self.current_token().type == token_type

    def match(self, *token_types):
        if self.current_token().type in token_types:
            return self.advance()

        return None

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        token = self.current_token()

        raise SyntaxError(
            f"{message} at line {token.line}, "
            f"column {token.column}. "
            f"Found {token.type.name}."
        )

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    def parse(self):
        self.skip_newlines()

        self.consume(
            TokenType.START,
            "Program must begin with START"
        )

        self.skip_newlines()

        statements = self.parse_block({TokenType.END})

        self.consume(
            TokenType.END,
            "Program must terminate with END"
        )

        self.skip_newlines()

        self.consume(
            TokenType.EOF,
            "Unexpected content after program END"
        )

        return Program(statements)

    def parse_block(self, terminators):
        statements = []

        while not self.check(TokenType.EOF):
            self.skip_newlines()

            if self.current_token().type in terminators:
                break

            statements.append(self.parse_statement())

            if not self.check(TokenType.NEWLINE):
                if self.current_token().type not in terminators:
                    raise SyntaxError(
                        f"Expected a new line at "
                        f"line {self.current_token().line}"
                    )

        return statements

    def parse_statement(self):
        if self.match(TokenType.LET):
            return self.parse_let()

        if self.match(TokenType.SET):
            return self.parse_set()

        if self.match(TokenType.PRINT):
            return self.parse_print()

        if self.match(TokenType.INPUT):
            return self.parse_input()

        if self.match(TokenType.IF):
            return self.parse_if()

        if self.match(TokenType.WHILE):
            return self.parse_while()

        token = self.current_token()

        raise SyntaxError(
            f"Unexpected token {token.type.name} "
            f"at line {token.line}, column {token.column}"
        )

    def parse_let(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name after LET"
        )

        self.consume(
            TokenType.ASSIGN,
            "Expected '=' after variable name"
        )

        value = self.parse_expression()

        return LetStatement(name.value, value)

    def parse_set(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name after SET"
        )

        self.consume(
            TokenType.ASSIGN,
            "Expected '=' after variable name"
        )

        value = self.parse_expression()

        return SetStatement(name.value, value)

    def parse_print(self):
        expression = self.parse_expression()

        return PrintStatement(expression)

    def parse_input(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name after INPUT"
        )

        prompt = None

        if self.match(TokenType.COMMA):
            prompt_token = self.consume(
                TokenType.STRING,
                "Expected a string prompt after comma"
            )

            prompt = prompt_token.value

        return InputStatement(name.value, prompt)

    def parse_if(self):
        condition = self.parse_expression()

        self.consume(
            TokenType.THEN,
            "Expected THEN after IF condition"
        )

        self.consume(
            TokenType.NEWLINE,
            "Expected new line after THEN"
        )

        then_branch = self.parse_block({
            TokenType.ELSE,
            TokenType.END
        })

        else_branch = []

        if self.match(TokenType.ELSE):
            self.consume(
                TokenType.NEWLINE,
                "Expected new line after ELSE"
            )

            else_branch = self.parse_block({TokenType.END})

        self.consume(
            TokenType.END,
            "Expected END IF"
        )

        self.consume(
            TokenType.IF,
            "Expected IF after END"
        )

        return IfStatement(
            condition,
            then_branch,
            else_branch
        )

    def parse_while(self):
        condition = self.parse_expression()

        self.consume(
            TokenType.DO,
            "Expected DO after WHILE condition"
        )

        self.consume(
            TokenType.NEWLINE,
            "Expected new line after DO"
        )

        body = self.parse_block({TokenType.END})

        self.consume(
            TokenType.END,
            "Expected END WHILE"
        )

        self.consume(
            TokenType.WHILE,
            "Expected WHILE after END"
        )

        return WhileStatement(condition, body)

    # Expression parsing

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        expression = self.parse_addition()

        operators = {
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
        }

        while self.current_token().type in operators:
            operator = self.advance()
            right = self.parse_addition()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_addition(self):
        expression = self.parse_multiplication()

        while self.check(TokenType.PLUS) or self.check(TokenType.MINUS):
            operator = self.advance()
            right = self.parse_multiplication()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_multiplication(self):
        expression = self.parse_unary()

        while self.current_token().type in {
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
        }:
            operator = self.advance()
            right = self.parse_unary()

            expression = BinaryExpression(
                expression,
                operator.value,
                right
            )

        return expression

    def parse_unary(self):
        if self.match(TokenType.MINUS):
            return UnaryExpression("-", self.parse_unary())

        if self.match(TokenType.PLUS):
            return UnaryExpression("+", self.parse_unary())

        return self.parse_primary()

    def parse_primary(self):
        token = self.advance()

        if token.type == TokenType.NUMBER:
            return NumberLiteral(token.value)

        if token.type == TokenType.STRING:
            return StringLiteral(token.value)

        if token.type == TokenType.BOOLEAN:
            return BooleanLiteral(token.value == "true")

        if token.type == TokenType.IDENTIFIER:
            return Identifier(token.value)

        if token.type == TokenType.LEFT_PAREN:
            expression = self.parse_expression()

            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected closing parenthesis"
            )

            return expression

        raise SyntaxError(
            f"Expected an expression at line {token.line}, "
            f"column {token.column}"
        )
