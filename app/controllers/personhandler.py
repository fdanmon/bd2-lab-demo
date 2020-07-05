class PersonHandler(object):
    def __init__(self):
        pass

    @classmethod
    def parse_info(cls, r):
        return {
            'id': r[0],
            'name': r[1],
            'document_number': r[2],
            'sex': r[3],
            'birth_date': r[4],
            'phone': r[5],
            'rating': r[6]
        }

    @classmethod
    def parse_skill(cls, r):
        return {
            'id': r[0],
            'rating': r[3],
            'person': {
                'id': r[4],
                'name': r[5],
                'document_number': r[6],
                'sex': r[7],
                'birth_date': r[8],
                'phone': r[9]
            },
            'skill': {
                'id': r[11],
                'title': r[13],
                'category': {
                    'id': r[14],
                    'name': r[15]
                }
            }
        }

    @classmethod
    def parse_average_rating(cls, r):
        return {
        'average_rating': r[7],
        'person': {
            'id': r[0],
            'name': r[1],
            'document_number': r[2],
            'sex': r[3],
            'birth_date': r[4],
            'phone': r[5]
        }
    }