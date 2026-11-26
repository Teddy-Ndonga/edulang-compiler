
import pytest

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import (
    SemanticAnalyzer,
    SemanticError,
)


def analyze_source(source):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()

    return analyzer.analyze(program)


def test_tracks_variable_types():
    source = """
START
    LET age = 20
    LET score = 85.5
    LET name = "Teddy"
    LET passed = true
END
"""

    symbols = analyze_source(source)

    assert symbols["age"] is int
    assert symbols["score"] is float
    assert symbols["name"] is str
    assert symbols["passed"] is bool


def test_rejects_undeclared_variable():
    source = """
START
    PRINT age
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_duplicate_variable_declaration():
    source = """
START
    LET age = 20
    LET age = 25
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_updating_undeclared_variable():
    source = """
START
    SET age = 25
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_incompatible_assignment():
    source = """
START
    LET age = 20
    SET age = "Teddy"
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_invalid_arithmetic():
    source = """
START
    LET result = "Hello" - 10
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_allows_string_concatenation():
    source = """
START
    LET name = "Teddy" + " Ndonga"
END
"""

    symbols = analyze_source(source)

    assert symbols["name"] is str


def test_allows_integer_to_decimal_assignment():
    source = """
START
    LET score = 85.5
    SET score = 90
END
"""

    symbols = analyze_source(source)

    assert symbols["score"] is float


def test_rejects_non_boolean_if_condition():
    source = """
START
    IF 10 THEN
        PRINT "Hello"
    END IF
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_non_boolean_while_condition():
    source = """
START
    WHILE 10 DO
        PRINT "Hello"
    END WHILE
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_rejects_input_into_undeclared_variable():
    source = """
START
    INPUT age
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)


def test_accepts_input_into_declared_variable():
    source = """
START
    LET age = 0
    INPUT age
END
"""

    symbols = analyze_source(source)

    assert symbols["age"] is int


def test_block_variables_are_local():
    source = """
START
    IF true THEN
        LET temporary = 10
    END IF

    PRINT temporary
END
"""

    with pytest.raises(SemanticError):
        analyze_source(source)
