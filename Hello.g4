// Define a grammar called Hello
grammar
Hello;
// GRAMMAR FOR I LANGUAGE

// starting point of parsing
program
    : {
    SimpleDeclaration | RoutineDeclaration
}
;

SimpleDeclaration
    : VariableDeclaration(NewLine | ';')
| TypeDeclaration(NewLine | ';')
;

VariableDeclaration
    : 'var'
Identifier
':'
Type ['is'
Expression
]
|
'var'
Identifier
'is'
Expression
;

TypeDeclaration
    : 'type'
Identifier
'is'
Type
;

Type
    : PrimitiveType
| UserType
| Identifier
;

PrimitiveType
    : 'integer'
| 'real'
| 'boolean'
;

UserType
    : ArrayType
| RecordType
;

RecordType
    : 'record'
{
    VariableDeclaration
}
'end'
;

ArrayType
    : 'array'
'['
Expression
']'
Type
;

Statement
    : Assignment
| RoutineCall
| WhileLoop
| ForLoop
| IfStatement
;

Assignment
    : ModifiablePrimary
':='
Expression
;

RoutineCall
    : Identifier ['('
Expression
{
    ','
    Expression
}
')'
]
;

WhileLoop
    : 'while'
Expression
'loop'
Body
'end'
;

ForLoop
    : 'for'
Identifier
'in' ['reverse']
Range
'loop'
Body
'end'
;

Range
    : Expression
'..'
Expression
;

IfStatement
    : 'if'
Expression
'then'
Body ['else'
Body
]
'end'
;

RoutineDeclaration
    : 'routine'
Identifier [Parameters] [':'
Type
]
['is' Body 'end']
;

Parameters
    : '('
ParameterDeclaration
{
    ','
    ParameterDeclaration
}
')'
;

ParameterDeclaration
    : Identifier
':'
Type
;


Body
    : {
    SimpleDeclaration | Statement
}
;

Expression
    : Relation
{
    ('and' | 'or' | 'xor')
    Relation
}
;

Relation
    : Simple [('<' | '<=' | '>' | '>=' | '=' | '/=')
Simple
]
;

Simple
    : Factor
{
    ('*' | '/' | '%')
    Factor
}
;
Factor
    : Summand
{
    ('+' | '-')
    Summand
}
;

Summand
    : Primary
| '('
Expression
')'
;

Primary
    : [Sign | 'not']
IntegerLiteral
| [Sign]
RealLiteral
| 'true'
| 'false'
| ModifiablePrimary
| RoutineCall
;

Sign
    : '+'
| '-'
;

ModifiablePrimary
    : Identifier
{
    '.'
    Identifier | '['
    Expression
    ']'
}
;


// TOKENS FOR LEXER

Identifier
    : Letter(Letter | DecimalDigit) *
;

Keyword
    : 'var'
| 'is'
| 'type'
| 'record'
| 'end'
| 'array'
| 'while'
| 'loop'
| 'for'
| 'in'
| 'reverse'
| 'if'
| 'then'
| 'else'
| 'not'
;

fragment
Letter
    : UnicodeLetter
| '_'
;

fragment
UnicodeLetter
    :[a - zA - Z]
;

BinaryOperator
    : 'and'
| 'or'
| 'xor'
| RelationalOperator
| MultiplicationOperator
| AdditionOperator
;

RelationalOperator
    : '<'
| '<='
| '>'
| '>='
| '='
| '/='
;

MultiplicationOperator
    :  '*'
| '/'
| '%'
;

AdditionOperator
    :  '+'
| '-'
;

IntegerLiteral
    : DecimalLiteral
| HexLiteral
;

RealLiteral
    : Decimals
'.'
Decimals ? Exponent ?
|
Decimals
Exponent
| '.'
Decimals
Exponent ?
;

fragment
Decimals
    : DecimalDigit +
;

fragment
Exponent
    : ('e' | 'E')('+' | '-') ? Decimals
;

fragment
DecimalLiteral
    : [1 - 9]
DecimalDigit *
;

fragment
HexLiteral
    : '0'('x' | 'X')
HexDigit +
;

fragment
DecimalDigit
    : [0 - 9]
;

fragment
HexDigit
    : [0 - 9a - fA - F]
;

fragment
NewLine
    : [\n
]
;

//
// > skip ; // skip spaces, tabs, newlines