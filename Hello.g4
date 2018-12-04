// Define a grammar called Hello
grammar Hello;
// GRAMMAR FOR I LANGUAGE

// starting point of parsing
program
    : (simpleDeclaration eos|routineDeclaration eos)*
    ;

simpleDeclaration
    : variableDeclaration
    | typeDeclaration
    ;

variableDeclaration
    : 'var' Identifier ':' lang_type ( 'is' expression )?
    | 'var' Identifier'is'expression
    ;

typeDeclaration
    : 'type' Identifier 'is' lang_type
    ;

lang_type
    : primitiveType
    | userType
    | Identifier
    ;

primitiveType
    : 'integer'
    | 'real'
    | 'boolean'
    ;

userType
    : arrayType
    | recordType
    ;

recordType
    : 'record' ( variableDeclaration )* 'end';

arrayType
    : 'array' '[' expression ']' lang_type
    ;

statement
    : assignment
    | routineCall
    | whileLoop
    | forLoop
    | ifStatement
    ;

assignment
    : modifiablePrimary ':=' expression
    ;

routineCall
    : Identifier ('(' expression ( ',' expression )* ')' )?
    ;

whileLoop
    : 'while' expression 'loop' body 'end'
    ;

forLoop
    : 'for' Identifier 'in' ('reverse')? lang_range 'loop' body 'end'
    ;

lang_range
    : expression '..' expression
    ;

ifStatement
    : 'if' expression 'then' body ('else' body )? 'end'
    ;

routineDeclaration
    : 'routine' Identifier (parameters)? (':' lang_type )? ('is' body ('return' expression )? 'end')?
    ;

parameters
    : '(' parameterDeclaration ( ',' parameterDeclaration )* ')'
    ;

parameterDeclaration
    : Identifier ':' lang_type
    ;

body
    : ( simpleDeclaration | statement )*
    ;

expression
    : relation ( ('and' | 'or' | 'xor') relation )*
    ;

relation
    : simple (('<' | '<=' | '>' | '>=' | '=' | '/=') simple )?
    ;

simple
    : factor ( ('*' | '/' | '%') factor )*
    ;

factor
    : summand ( ('+' | '-') summand )*
    ;

summand
    : primary
    | '(' expression ')'
    ;

primary
    : ( ('+' | '-') | 'not')? IntegerLiteral
    | ('+' | '-')? RealLiteral
    | 'true'
    | 'false'
    | modifiablePrimary
    | routineCall
    ;


modifiablePrimary
    : Identifier ( '.' Identifier | '[' expression ']' )*
    ;

eos
    : ';'
    | EOF
    ;


// TOKENS FOR LEXER


fragment Sign
    : '+'
    | '-'
    ;

Identifier
    : Letter(Letter | DecimalDigit)*
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
    | 'return'
    ;

fragment Letter
    : UnicodeLetter
    | '_'
    ;

fragment UnicodeLetter
    :[a-zA-Z]
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
    : '+'
    | '-'
    ;

IntegerLiteral
    : DecimalLiteral
    | HexLiteral
    ;

RealLiteral
    : Decimals '.' Decimals ? Exponent ?
    | Decimals Exponent
    | '.' Decimals Exponent ?
    ;

fragment Decimals
    : DecimalDigit+
    ;

fragment Exponent
    : ('e' | 'E')('+' | '-') ? Decimals
    ;

fragment DecimalLiteral
    : '0' | ([1-9]DecimalDigit*)
    ;

fragment HexLiteral
    : '0'('x' | 'X') HexDigit+
    ;

fragment DecimalDigit
    : [0-9]
    ;

fragment HexDigit
    : [0-9a-fA-F]
    ;

WHITE_SPACE  :  [ \t]+ -> channel(HIDDEN)
    ;

COMMENT // Multiline
    :   '/*' .*? '*/' -> channel(HIDDEN)
    ;

LINE_COMMENT // Single line
    :   '//' ~[\r\n]* -> skip
    ;

TERMINATOR
	: [\r\n]+ -> channel(HIDDEN)
	;

//
// > skip ; // skip spaces, tabs, newlines