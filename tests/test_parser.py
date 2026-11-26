
import pytest

from src.lexer import Lexer
from src.parser import Parser
from src.ast_nodes import (
    Program,
    LetStatement,
    PrintStatement,
    BinaryExpression,
    NumberLiteral,
    IfStatement,
    WhileStatement,
)


def parse_source(source):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_parses_simple_program():
    source = """
START
    LET age = 20
    PRINT age
END
"""

    program = parse_source(source)

    assert isinstance(program, Program)
    assert len(program.statements) == 2


def test_parses_variable_declaration():
    source = """
START
    LET age = 20
END
"""

    program = parse_source(source)

    statement = program.statements[0]

    assert isinstance(statement, LetStatement)
    assert statement.name == "age"
    assert isinstance(statement.value, NumberLiteral)
    assert statement.value.value == 20


def test_parses_arithmetic_expression():
    source = """
START
    LET result = 10 + 5 * 2
END
"""

    program = parse_source(source)

    expression = program.statements[0].value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"
    assert isinstance(expression.right, BinaryExpression)
    assert expression.right.operator == "*"


def test_respects_parentheses():
    source = """
START
    LET result = (10 + 5) * 2
END
"""

    program = parse_source(source)

    expression = program.statements[0].value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "*"
    assert expression.left.operator == "+"


def test_parses_print_statement():
    source = """
START
    PRINT 100
END
"""

    program = parse_source(source)

    assert isinstance(program.statements[0], PrintStatement)


def test_parses_if_statement():
    source = """
START
    LET age = 20

    IF age >= 18 THEN
        PRINT "Eligible"
    ELSE
        PRINT "Not eligible"
    END IF
END
"""

    program = parse_source(source)

    statement = program.statements[1]

    assert isinstance(statement, IfStatement)
    assert len(statement.then_branch) == 1
    assert len(statement.else_branch) == 1


def test_parses_while_statement():
    source = """
START
    LET counter = 1

    WHILE counter <= 5 DO
        SET counter = counter + 1
    END WHILE
END
"""

    program = parse_source(source)

    statement = program.statements[1]

    assert isinstance(statement, WhileStatement)
    assert len(statement.body) == 1


def test_rejects_missing_program_start():
    source = """
LET age = 20
END
"""

    with pytest.raises(SyntaxError):
        parse_source(source)


def test_rejects_missing_program_end():
    source = """
START
    LET age = 20
"""

    with pytest.raises(SyntaxError):
        parse_source(source)


def test_rejects_invalid_variable_declaration():
    source = """
START
    LET = 20
END
"""

    with pytest.raises(SyntaxError):
        parse_source(source)


def test_rejects_missing_then():
    source = """
START
    IF 10 > 5
        PRINT "Hello"
    END IF
END
"""

    with pytest.raises(SyntaxError):
        parse_source(source)


def test_rejects_unclosed_parenthesis():
    source = """
START
    LET result = (10 + 5
END
"""

    with pytest.raises(SyntaxError):
        parse_source(source)
