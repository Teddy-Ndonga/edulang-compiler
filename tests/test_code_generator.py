
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator


def compile_source(source):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    symbols = analyzer.analyze(program)

    generator = CodeGenerator(symbols)
    return generator.generate(program)


def test_generates_variable_declaration():
    source = """
START
    LET age = 20
END
"""
    result = compile_source(source)

    assert result == "age = 20\n"


def test_generates_variable_assignment():
    source = """
START
    LET age = 20
    SET age = 25
END
"""
    result = compile_source(source)

    assert "age = 25" in result


def test_generates_print_statement():
    source = """
START
    PRINT "Hello EduLang"
END
"""
    result = compile_source(source)

    assert "print('Hello EduLang')" in result


def test_generates_arithmetic_expression():
    source = """
START
    LET total = 10 + 5 * 2
END
"""
    result = compile_source(source)

    assert "total = (10 + (5 * 2))" in result


def test_generates_boolean_values():
    source = """
START
    LET passed = true
END
"""
    result = compile_source(source)

    assert "passed = True" in result


def test_generates_input_statement():
    source = """
START
    LET age = 0
    INPUT age
END
"""
    result = compile_source(source)

    assert "age = int(input())" in result


def test_generates_decimal_input():
    source = """
START
    LET score = 0.0
    INPUT score
END
"""
    result = compile_source(source)

    assert "score = float(input())" in result


def test_generates_string_input():
    source = """
START
    LET name = ""
    INPUT name
END
"""
    result = compile_source(source)

    assert "name = input()" in result


def test_generates_if_statement():
    source = """
START
    LET age = 20

    IF age >= 18 THEN
        PRINT "Adult"
    END IF
END
"""
    result = compile_source(source)

    assert "if (age >= 18):" in result
    assert "    print('Adult')" in result


def test_generates_if_else_statement():
    source = """
START
    LET age = 16

    IF age >= 18 THEN
        PRINT "Adult"
    ELSE
        PRINT "Minor"
    END IF
END
"""
    result = compile_source(source)

    assert "if (age >= 18):" in result
    assert "else:" in result
    assert "print('Minor')" in result


def test_generates_while_loop():
    source = """
START
    LET count = 0

    WHILE count < 3 DO
        PRINT count
        SET count = count + 1
    END WHILE
END
"""
    result = compile_source(source)

    assert "while (count < 3):" in result
    assert "    print(count)" in result
    assert "    count = (count + 1)" in result


def test_generated_python_is_valid():
    source = """
START
    LET age = 20

    IF age >= 18 THEN
        PRINT "Adult"
    ELSE
        PRINT "Minor"
    END IF
END
"""
    result = compile_source(source)

    compile(result, "<edulang>", "exec")
