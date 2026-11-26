
import argparse
import sys
from pathlib import Path

from src.compiler import Compiler
from src.semantic_analyzer import SemanticError
from src.code_generator import CodeGenerationError


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="EduLang compiler - compile .edu files into Python."
    )

    parser.add_argument(
        "source",
        help="Path to the EduLang source file (.edu)"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Path for the generated Python file"
    )

    args = parser.parse_args(argv)

    source_path = Path(args.source)

    if source_path.suffix.lower() != ".edu":
        print("Error: Source file must have a .edu extension.", file=sys.stderr)
        return 1

    output_path = (
        Path(args.output)
        if args.output
        else source_path.with_suffix(".py")
    )

    try:
        source_code = source_path.read_text(encoding="utf-8")

        compiler = Compiler()
        python_code = compiler.compile(source_code)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(python_code, encoding="utf-8")

        print(f"Compilation successful: {source_path}")
        print(f"Generated Python file: {output_path}")

        return 0

    except (OSError, SyntaxError, SemanticError, CodeGenerationError) as error:
        print(f"Compilation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
