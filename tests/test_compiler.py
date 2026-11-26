
from src.compiler import Compiler


def test_compiles_simple_program():
    source = """
START
    LET score = 85
    PRINT score
END
"""
    compiler = Compiler()
    result = compiler.compile(source)

    assert result == "score = 85\nprint(score)\n"


def test_compiles_arithmetic_program():
    source = """
START
    LET total = 10 + 5
    PRINT total
END
"""
    compiler = Compiler()
    result = compiler.compile(source)

    assert "total = (10 + 5)" in result
    assert "print(total)" in result


def test_compiles_conditional_program():
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
    compiler = Compiler()
    result = compiler.compile(source)

    assert "if (age >= 18):" in result
    assert "else:" in result


def test_compiles_loop_program():
    source = """
START
    LET count = 0

    WHILE count < 3 DO
        PRINT count
        SET count = count + 1
    END WHILE
END
"""
    compiler = Compiler()
    result = compiler.compile(source)

    assert "while (count < 3):" in result


def test_compiler_rejects_semantic_errors():
    source = """
START
    PRINT unknown_variable
END
"""
    compiler = Compiler()

    try:
        compiler.compile(source)
        assert False, "Expected a semantic error"
    except Exception as error:
        assert "declared" in str(error)


def test_compiler_generates_valid_python():
    source = """
START
    LET score = 85
    PRINT score
END
"""
    compiler = Compiler()
    result = compiler.compile(source)

    compile(result, "<edulang>", "exec")
