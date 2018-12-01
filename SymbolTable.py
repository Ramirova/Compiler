class SymbolTable:

    root_table = None

    def __init__(self, parent):
        if not (SymbolTable.root_table is None and parent is None):
            raise Exception
        if parent is None and SymbolTable.root_table is None:
            SymbolTable.root_table = self
        self.parent_scope = parent
        self.scope = {}
        self.child_scopes = {}

    def add(self, variable_name, variable_type):
        self.scope[variable_name] = SymbolTableEntry(False, variable_type, variable_name)

    def remove(self, variable_name):
        self.scope[variable_name] = None

    def set_used(self, variable_name):
        if not self.is_defined_in_scope(variable_name):
            raise Exception
        else:
            self.scope[variable_name].used = True

    def create_child_scope(self, scope_name):
        self.child_scopes[scope_name] = SymbolTable(self)
        return self.child_scopes[scope_name]

    def is_defined_in_scope(self, variable_name):
        if self.scope[variable_name] is None:
            return False
        else:
            return True


class SymbolTableEntry:
    def __init__(self, used, variable_type, variable_name):
        self.used = used
        # self.initializer = initializer
        self.variable_type = variable_type
        self.variable_name = variable_name
        # self.value = value

