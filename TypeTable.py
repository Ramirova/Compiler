class TypeTable:

    table = None

    def __init__(self, ):
        self.types = {}
        if TypeTable.table is None:
            TypeTable.table = self

    def add_type(self, type_id, type_content):
        self.types[type_id] = type_content


class PrimitiveType:
    integer = 1
    real = 2
    boolean = 3

    def __init__(self):
        pass


class ArrayType:

    def __init__(self, nested_type):

        self.nested_type_id = 0

        if type(nested_type) is PrimitiveType:
            self.nested_type_id = nested_type

        if type(nested_type) is ArrayType:
            self.nested_type_id = nested_type.get_hash()
            pass

        TypeTable.table.types[self.get_id()] = self

    def get_id(self):
        return hash(self.nested_type_id)


class RecordType:

    def __init__(self, nested_type):
        if type(nested_type) is PrimitiveType:
            self.nested_type_id = nested_type

        if type(nested_type) is ArrayType:
            self.nested_type_id = nested_type.get_hash()
            pass

        TypeTable.table.types[self.get_hash()] = self

    def get_hash(self):
        return hash(self.nested_type_id)




c = {'a': 12345, 'b': 3466443}
d = {'a': 12345, 'b': 3466443}

print(hash(frozenset(c.items())), hash(frozenset(d.items())))