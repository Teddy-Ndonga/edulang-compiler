
from src.main import main


def test_cli_compiles_edu_file(tmp_path, capsys):
    source_file = tmp_path / "hello.edu"
    source_file.write_text(
        'START\n    PRINT "Hello EduLang"\nEND\n',
        encoding="utf-8"
    )

    result = main([str(source_file)])

    output_file = tmp_path / "hello.py"

    assert result == 0
    assert output_file.exists()
    assert "print('Hello EduLang')" in output_file.read_text(
        encoding="utf-8"
    )

    captured = capsys.readouterr()
    assert "Compilation successful" in captured.out


def test_cli_accepts_custom_output_path(tmp_path):
    source_file = tmp_path / "hello.edu"
    output_file = tmp_path / "generated" / "program.py"

    source_file.write_text(
        'START\n    PRINT "Hello"\nEND\n',
        encoding="utf-8"
    )

    result = main([
        str(source_file),
        "--output",
        str(output_file)
    ])

    assert result == 0
    assert output_file.exists()


def test_cli_rejects_non_edu_file(tmp_path, capsys):
    source_file = tmp_path / "program.txt"
    source_file.write_text("Some text", encoding="utf-8")

    result = main([str(source_file)])

    assert result == 1
    assert "must have a .edu extension" in capsys.readouterr().err


def test_cli_handles_missing_file(tmp_path, capsys):
    source_file = tmp_path / "missing.edu"

    result = main([str(source_file)])

    assert result == 1
    assert "Compilation failed" in capsys.readouterr().err


def test_cli_handles_syntax_error(tmp_path, capsys):
    source_file = tmp_path / "invalid.edu"
    source_file.write_text(
        'START\n    LET = 10\nEND\n',
        encoding="utf-8"
    )

    result = main([str(source_file)])

    assert result == 1
    assert "Compilation failed" in capsys.readouterr().err


def test_cli_handles_semantic_error(tmp_path, capsys):
    source_file = tmp_path / "invalid.edu"
    source_file.write_text(
        "START\n    PRINT unknown_variable\nEND\n",
        encoding="utf-8"
    )

    result = main([str(source_file)])

    assert result == 1
    assert "Compilation failed" in capsys.readouterr().err


def test_cli_executes_generated_program(tmp_path, capsys):
    source_file = tmp_path / "hello.edu"

    source_file.write_text(
        'START\n'
        '    PRINT "Hello from EduLang!"\n'
        'END\n',
        encoding="utf-8"
    )

    result = main([str(source_file), "--run"])

    assert result == 0

    captured = capsys.readouterr()
    assert "Hello from EduLang!" in captured.out
    assert "Executing program..." in captured.out


def test_cli_returns_error_for_runtime_failure(tmp_path, capsys):
    source_file = tmp_path / "runtime_error.edu"

    source_file.write_text(
        "START\n"
        "    LET result = 10 / 0\n"
        "    PRINT result\n"
        "END\n",
        encoding="utf-8"
    )

    result = main([str(source_file), "--run"])

    assert result != 0

    captured = capsys.readouterr()
    assert "ZeroDivisionError" in captured.err
