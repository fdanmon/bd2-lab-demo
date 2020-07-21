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
    def parse(cls, p):
        return {
            'id': p.id,
            'name': p.name,
            'document_number': p.document_number,
            'sex': p.sex,
            'birth_date': p.birth_date,
            'phone': p.phone,
            'rating': p.rating
        }

    @classmethod
    def parse_skill(cls, r):
        return {
            'id': r[1],
            'title': r[2],
            'rating': r[3],
            'category': {
                'id': r[4],
                'name': r[5]
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