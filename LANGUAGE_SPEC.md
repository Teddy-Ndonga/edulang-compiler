
# EduLang Language Specification

Version: 1.0

## 1. Introduction

EduLang is a small educational programming language designed to
demonstrate programming language design and compiler construction.

Its compiler will be implemented in Python and will initially
translate EduLang source code into Python code.

## 2. Program Structure

Every EduLang program must begin with START and terminate with END.

Example:

START
    PRINT "Hello, World!"
END

## 3. Keywords

- START: Begins a program.
- END: Terminates a program.
- LET: Declares a variable.
- SET: Updates an existing variable.
- PRINT: Displays output.
- INPUT: Reads user input.
- IF: Begins a conditional statement.
- ELSE: Defines an alternative branch.
- THEN: Separates an IF condition from its body.
- END IF: Terminates a conditional statement.
- WHILE: Begins a loop.
- DO: Separates a loop condition from its body.
- END WHILE: Terminates a loop.

## 4. Data Types

- Integer
- Decimal
- String
- Boolean

Boolean values: true and false.

## 5. Operators

Arithmetic:
+ - * / %

Comparison:
== != > < >= <=

## 6. Variables

Variables are declared using LET.

Example:
LET age = 23

Existing variables are updated using SET.

Example:
SET age = 24

Variable names must begin with a letter or underscore.

## 7. Output

PRINT displays a value or expression.

Example:
PRINT "Hello"
PRINT 10 + 20

## 8. Input

INPUT reads a value from the user.

Example:
INPUT age

## 9. Conditional Statements

IF condition THEN
    statements
ELSE
    statements
END IF

ELSE is optional.

## 10. Loops

WHILE condition DO
    statements
END WHILE

## 11. Comments

Comments begin with #.

Example:
# This is a comment

## 12. Source Files

EduLang source files use the .edu extension.

## 13. Compilation Target

The initial compiler target is Python.
