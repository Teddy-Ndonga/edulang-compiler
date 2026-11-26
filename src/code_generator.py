
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


class CodeGenerationError(Exception):
    """Raised when Python code cannot be generated."""
    pass


class CodeGenerator:
    def __init__(self, symbols=None):
        self.symbols = symbols or {}

    def generate(self, program):
        if not isinstance(program, Program):
            raise CodeGenerationError("Expected a Program node")

        lines = self.generate_statements(program.statements)

        if not lines:
            lines = ["pass"]

        return "\n".join(lines) + "\n"

    def generate_statements(self, statements, indent=0):
        lines = []

        for statement in statements:
            lines.extend(self.generate_statement(statement, indent))

        return lines

    def generate_statement(self, statement, indent):
        prefix = "    " * indent

        if isinstance(statement, LetStatement):
            value = self.generate_expression(statement.value)
            return [f"{prefix}{statement.name} = {value}"]

        if isinstance(statement, SetStatement):
            value = self.generate_expression(statement.value)
            return [f"{prefix}{statement.name} = {value}"]

        if isinstance(statement, PrintStatement):
            expression = self.generate_expression(statement.expression)
            return [f"{prefix}print({expression})"]

        if isinstance(statement, InputStatement):
            return [
                self.generate_input(
                    statement.name,
                    prefix,
                    statement.prompt
                )
            ]

        if isinstance(statement, IfStatement):
            return self.generate_if(statement, indent)

        if isinstance(statement, WhileStatement):
            return self.generate_while(statement, indent)

        raise CodeGenerationError(
            f"Unsupported statement: {type(statement).__name__}"
        )

    def generate_input(self, name, prefix, prompt=None):
        variable_type = self.symbols.get(name)

        prompt_argument = repr(prompt) if prompt is not None else ""

        if variable_type is int:
            conversion = f"int(input({prompt_argument}))"

        elif variable_type is float:
            conversion = f"float(input({prompt_argument}))"

        elif variable_type is bool:
            conversion = (
                f'input({prompt_argument}).strip().lower() == "true"'
            )

        elif variable_type is str:
            conversion = f"input({prompt_argument})"

        else:
            raise CodeGenerationError(
                f"Unknown type for input variable '{name}'"
            )

        return f"{prefix}{name} = {conversion}"

    def generate_if(self, statement, indent):
        prefix = "    " * indent
        condition = self.generate_expression(statement.condition)

        lines = [f"{prefix}if {condition}:"]

        then_lines = self.generate_statements(
            statement.then_branch, indent + 1
        )
        lines.extend(then_lines or ["    " * (indent + 1) + "pass"])

        if statement.else_branch:
            lines.append(f"{prefix}else:")

            else_lines = self.generate_statements(
                statement.else_branch, indent + 1
            )
            lines.extend(else_lines or ["    " * (indent + 1) + "pass"])

        return lines

    def generate_while(self, statement, indent):
        prefix = "    " * indent
        condition = self.generate_expression(statement.condition)

        lines = [f"{prefix}while {condition}:"]

        body_lines = self.generate_statements(
            statement.body, indent + 1
        )
        lines.extend(body_lines or ["    " * (indent + 1) + "pass"])

        return lines

    def generate_expression(self, expression):
        if isinstance(expression, NumberLiteral):
            return repr(expression.value)

        if isinstance(expression, StringLiteral):
            return repr(expression.value)

        if isinstance(expression, BooleanLiteral):
            return "True" if expression.value else "False"

        if isinstance(expression, Identifier):
            return expression.name

        if isinstance(expression, UnaryExpression):
            operand = self.generate_expression(expression.operand)
            return f"({expression.operator}{operand})"

        if isinstance(expression, BinaryExpression):
            left = self.generate_expression(expression.left)
            right = self.generate_expression(expression.right)

            return f"({left} {expression.operator} {right})"

        raise CodeGenerationError(
            f"Unsupported expression: {type(expression).__name__}"
        )
