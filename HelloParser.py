# Generated from Hello.g4 by ANTLR 4.7.1
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3")
        buf.write(u"%\7\4\2\t\2\3\2\3\2\3\2\2\2\3\2\2\2\2\5\2\4\3\2\2\2\4")
        buf.write(u"\5\b\2\1\2\5\3\3\2\2\2\2")
        return buf.getvalue()


class HelloParser(Parser):
    grammarFileName = "Hello.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = []

    symbolicNames = [u"<INVALID>", u"SimpleDeclaration", u"VariableDeclaration",
                     u"TypeDeclaration", u"Type", u"PrimitiveType", u"UserType",
                     u"RecordType", u"ArrayType", u"Statement", u"Assignment",
                     u"RoutineCall", u"WhileLoop", u"ForLoop", u"Range",
                     u"IfStatement", u"RoutineDeclaration", u"Parameters",
                     u"ParameterDeclaration", u"Body", u"Expression", u"Relation",
                     u"Simple", u"Factor", u"Summand", u"Primary", u"Sign",
                     u"ModifiablePrimary", u"Identifier", u"Keyword", u"BinaryOperator",
                     u"RelationalOperator", u"MultiplicationOperator",
                     u"AdditionOperator", u"IntegerLiteral", u"RealLiteral"]

    RULE_program = 0

    ruleNames = [u"program"]

    EOF = Token.EOF
    SimpleDeclaration = 1
    VariableDeclaration = 2
    TypeDeclaration = 3
    Type = 4
    PrimitiveType = 5
    UserType = 6
    RecordType = 7
    ArrayType = 8
    Statement = 9
    Assignment = 10
    RoutineCall = 11
    WhileLoop = 12
    ForLoop = 13
    Range = 14
    IfStatement = 15
    RoutineDeclaration = 16
    Parameters = 17
    ParameterDeclaration = 18
    Body = 19
    Expression = 20
    Relation = 21
    Simple = 22
    Factor = 23
    Summand = 24
    Primary = 25
    Sign = 26
    ModifiablePrimary = 27
    Identifier = 28
    Keyword = 29
    BinaryOperator = 30
    RelationalOperator = 31
    MultiplicationOperator = 32
    AdditionOperator = 33
    IntegerLiteral = 34
    RealLiteral = 35

    def __init__(self, input, output=sys.stdout):
        super(HelloParser, self).__init__(input, output=output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(HelloParser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return HelloParser.RULE_program

        def enterRule(self, listener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)

    def program(self):

        localctx = HelloParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            SimpleDeclaration | RoutineDeclaration

    except RecognitionException as re:
    localctx.exception = re
    self._errHandler.reportError(self, re)
    self._errHandler.recover(self, re)

finally:
self.exitRule()
return localctx
