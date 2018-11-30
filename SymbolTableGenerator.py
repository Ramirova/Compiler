from HelloVisitor import HelloVisitor

class SymbolTableGenerator(HelloVisitor):

    def visitProgram(self, ctx):
        return