class CompanyHandler(object):
    def __init__(self):
        pass
    
    @classmethod
    def parse_info(cls, e):
        return {
            'id': e.id,
            'name': e.name,
            'document_number': e.document_number,
            'category_id': e.category_id,
            'rating': e.rating,
            'phone': e.rating
        }
