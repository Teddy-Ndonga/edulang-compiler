
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator


class Compiler:
    """Coordinates the EduLang compilation pipeline."""

    def compile(self, source):
        # Stage 1: Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Stage 2: Syntax analysis
        parser = Parser(tokens)
        program = parser.parse()

        # Stage 3: Semantic analysis
        analyzer = SemanticAnalyzer()
        symbols = analyzer.analyze(program)

        # Stage 4: Code generation
        generator = CodeGenerator(symbols)
        python_code = generator.generate(program)

        return python_code
