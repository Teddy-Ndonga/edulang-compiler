# This file will define the different types of nodes that can appear in our syntax tree.


from dataclasses import dataclass, field


class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class Program(ASTNode):
    statements: list = field(default_factory=list)


# Statements

@dataclass
class LetStatement(ASTNode):
    name: str
    value: ASTNode


@dataclass
class SetStatement(ASTNode):
    name: str
    value: ASTNode


@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode


@dataclass
class InputStatement(ASTNode):
    name: str
    prompt: str | None = None


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: list
    else_branch: list = field(default_factory=list)


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: list


# Expressions

@dataclass
class NumberLiteral(ASTNode):
    value: int | float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryExpression(ASTNode):
    operator: str
    operand: ASTNode
