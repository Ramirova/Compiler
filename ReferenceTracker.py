class ReferenceTracker:
    def __init__(self):
        self.reference_count_table = {}

    def increment_reference(self, object_id):
        if self.is_referenced(object_id):
            self.reference_count_table[object_id] = 1
        else:
            self.reference_count_table[object_id] += 1

    def decrement_reference(self, object_id):
        if self.is_referenced(object_id):
            raise Exception("object with id {} is not referenced".format(object_id))
        elif self.reference_count_table[object_id] == 1:
            del self.reference_count_table[object_id]
        else:
            self.reference_count_table[object_id] -= 1

    def count_references(self, object_id):
        if self.is_referenced(object_id):
            return 0
        else:
            return self.reference_count_table[object_id]

    def is_referenced(self, object_id):
        return object_id in self.reference_count_table.keys()
