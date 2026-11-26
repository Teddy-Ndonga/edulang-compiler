
import pytest

from src.lexer import Lexer
from src.tokens import TokenType


def test_recognizes_keywords():
    source = "START LET SET PRINT INPUT END"

    tokens = Lexer(source).tokenize()

    types = [token.type for token in tokens]

    assert types == [
        TokenType.START,
        TokenType.LET,
        TokenType.SET,
        TokenType.PRINT,
        TokenType.INPUT,
        TokenType.END,
        TokenType.EOF,
    ]


def test_recognizes_numbers():
    source = "LET age = 20"

    tokens = Lexer(source).tokenize()

    assert tokens[3].type == TokenType.NUMBER
    assert tokens[3].value == 20


def test_recognizes_decimal_numbers():
    source = "LET score = 85.5"

    tokens = Lexer(source).tokenize()

    assert tokens[3].type == TokenType.NUMBER
    assert tokens[3].value == 85.5


def test_recognizes_strings():
    source = 'LET name = "Teddy"'

    tokens = Lexer(source).tokenize()

    assert tokens[3].type == TokenType.STRING
    assert tokens[3].value == "Teddy"


def test_recognizes_arithmetic_operators():
    source = "10 + 5 - 2 * 3 / 1 % 2"

    tokens = Lexer(source).tokenize()

    types = [token.type for token in tokens[:-1]]

    assert types == [
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.MINUS,
        TokenType.NUMBER,
        TokenType.MULTIPLY,
        TokenType.NUMBER,
        TokenType.DIVIDE,
        TokenType.NUMBER,
        TokenType.MODULO,
        TokenType.NUMBER,
    ]


def test_recognizes_comparison_operators():
    source = "== != > < >= <="

    tokens = Lexer(source).tokenize()

    types = [token.type for token in tokens[:-1]]

    assert types == [
        TokenType.EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.GREATER,
        TokenType.LESS,
        TokenType.GREATER_EQUAL,
        TokenType.LESS_EQUAL,
    ]


def test_recognizes_boolean_values():
    source = "true false"

    tokens = Lexer(source).tokenize()

    assert tokens[0].type == TokenType.BOOLEAN
    assert tokens[1].type == TokenType.BOOLEAN


def test_ignores_comments():
    source = "LET age = 20 # This is a comment"

    tokens = Lexer(source).tokenize()

    types = [token.type for token in tokens]

    assert TokenType.LET in types
    assert TokenType.NUMBER in types
    assert TokenType.IDENTIFIER in types
    assert TokenType.EOF in types


def test_raises_error_for_unexpected_character():
    source = "LET age = 20 @"

    with pytest.raises(SyntaxError):
        Lexer(source).tokenize()


def test_raises_error_for_unterminated_string():
    source = 'LET name = "Teddy'

    with pytest.raises(SyntaxError):
        Lexer(source).tokenize()
