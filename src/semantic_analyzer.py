
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


class SemanticError(Exception):
    """Raised when a semantic error is detected."""
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}

    def analyze(self, program):
        if not isinstance(program, Program):
            raise SemanticError("Expected a Program node")

        self.symbols = {}

        self.analyze_statements(program.statements, self.symbols)

        return self.symbols

    def analyze_statements(self, statements, symbols):
        for statement in statements:

            if isinstance(statement, LetStatement):
                self.analyze_let(statement, symbols)

            elif isinstance(statement, SetStatement):
                self.analyze_set(statement, symbols)

            elif isinstance(statement, PrintStatement):
                self.infer_type(statement.expression, symbols)

            elif isinstance(statement, InputStatement):
                self.analyze_input(statement, symbols)

            elif isinstance(statement, IfStatement):
                self.analyze_if(statement, symbols)

            elif isinstance(statement, WhileStatement):
                self.analyze_while(statement, symbols)

            else:
                raise SemanticError(
                    f"Unsupported statement: {type(statement).__name__}"
                )

    def analyze_let(self, statement, symbols):
        name = statement.name

        if name in symbols:
            raise SemanticError(
                f"Variable '{name}' has already been declared"
            )

        variable_type = self.infer_type(
            statement.value, symbols
        )

        symbols[name] = variable_type

    def analyze_set(self, statement, symbols):
        name = statement.name

        if name not in symbols:
            raise SemanticError(
                f"Cannot update undeclared variable '{name}'"
            )

        new_type = self.infer_type(
            statement.value, symbols
        )

        existing_type = symbols[name]

        if not self.types_compatible(existing_type, new_type):
            raise SemanticError(
                f"Cannot assign {new_type.__name__} "
                f"to variable '{name}' of type "
                f"{existing_type.__name__}"
            )

    def analyze_input(self, statement, symbols):
        name = statement.name

        if name not in symbols:
            raise SemanticError(
                f"Cannot read input into undeclared variable '{name}'"
            )

    def analyze_if(self, statement, symbols):
        condition_type = self.infer_type(
            statement.condition, symbols
        )

        if condition_type is not bool:
            raise SemanticError(
                "IF condition must evaluate to a boolean"
            )

        # Each branch receives its own symbol table.
        then_symbols = symbols.copy()
        else_symbols = symbols.copy()

        self.analyze_statements(
            statement.then_branch, then_symbols
        )

        self.analyze_statements(
            statement.else_branch, else_symbols
        )

    def analyze_while(self, statement, symbols):
        condition_type = self.infer_type(
            statement.condition, symbols
        )

        if condition_type is not bool:
            raise SemanticError(
                "WHILE condition must evaluate to a boolean"
            )

        # Variables declared inside the loop remain local.
        loop_symbols = symbols.copy()

        self.analyze_statements(
            statement.body, loop_symbols
        )

    def types_compatible(self, target_type, value_type):
        if target_type == value_type:
            return True

        # An integer can be assigned to a decimal variable.
        if target_type is float and value_type is int:
            return True

        return False

    def infer_type(self, expression, symbols):

        if isinstance(expression, NumberLiteral):
            if isinstance(expression.value, int):
                return int

            return float

        if isinstance(expression, StringLiteral):
            return str

        if isinstance(expression, BooleanLiteral):
            return bool

        if isinstance(expression, Identifier):
            if expression.name not in symbols:
                raise SemanticError(
                    f"Variable '{expression.name}' "
                    "has not been declared"
                )

            return symbols[expression.name]

        if isinstance(expression, UnaryExpression):
            operand_type = self.infer_type(
                expression.operand, symbols
            )

            if operand_type not in (int, float):
                raise SemanticError(
                    "Unary operators require a numeric operand"
                )

            return operand_type

        if isinstance(expression, BinaryExpression):
            left_type = self.infer_type(
                expression.left, symbols
            )

            right_type = self.infer_type(
                expression.right, symbols
            )

            return self.infer_binary_type(
                expression.operator,
                left_type,
                right_type
            )

        raise SemanticError(
            f"Unsupported expression: {type(expression).__name__}"
        )

    def infer_binary_type(self, operator, left_type, right_type):

        numeric_types = (int, float)

        # Addition
        if operator == "+":
            if left_type in numeric_types and right_type in numeric_types:
                if float in (left_type, right_type):
                    return float

                return int

            if left_type is str and right_type is str:
                return str

            raise SemanticError(
                "Addition requires two numbers or two strings"
            )

        # Subtraction, multiplication and division
        if operator in ("-", "*", "/", "%"):
            if left_type not in numeric_types or right_type not in numeric_types:
                raise SemanticError(
                    f"Operator '{operator}' requires numeric operands"
                )

            if operator == "/":
                return float

            if float in (left_type, right_type):
                return float

            return int

        # Equality and inequality
        if operator in ("==", "!="):
            compatible = (
                left_type == right_type
                or (
                    left_type in numeric_types
                    and right_type in numeric_types
                )
            )

            if not compatible:
                raise SemanticError(
                    f"Incompatible types for '{operator}'"
                )

            return bool

        # Greater than, less than and related comparisons
        if operator in (">", "<", ">=", "<="):
            if left_type not in numeric_types or right_type not in numeric_types:
                raise SemanticError(
                    f"Operator '{operator}' requires numeric operands"
                )

            return bool

        raise SemanticError(
            f"Unknown binary operator '{operator}'"
        )
