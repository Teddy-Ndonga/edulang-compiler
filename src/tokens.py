
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Program structure
    START = auto()
    END = auto()

    # Variables and output
    LET = auto()
    SET = auto()
    PRINT = auto()
    INPUT = auto()

    # Conditional statements
    IF = auto()
    ELSE = auto()
    THEN = auto()

    # Loops
    WHILE = auto()
    DO = auto()

    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()

    # Identifiers
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    # Comparison operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()

    # Assignment
    ASSIGN = auto()

    # Special tokens
    NEWLINE = auto()
    EOF = auto()

    COMMA = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token({self.type.name}, {self.value!r}, "
            f"line={self.line}, column={self.column})"
        )
