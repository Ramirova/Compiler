class ObjectService:

    last_id = 0

    def __init__(self):
        pass

    @staticmethod
    def get_id():
        ObjectService.last_id += 1
        return ObjectService.last_id
