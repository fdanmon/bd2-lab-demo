class CategoryHandler(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, c):
        return {
            'id': c.id,
            'name': c.name
        }