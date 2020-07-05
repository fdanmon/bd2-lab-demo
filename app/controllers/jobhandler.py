class JobHandler(object):
    def __init__(self):
        pass
    
    @classmethod
    def parse_job_info(cls, r):
        return {
            'id': r[0],
            'title': r[1],
            'description': r[2],
            'vacancies': r[3],
            'category': {
                'id': r[8],
                'title': r[9]
            },
            'company': {
                'id': r[10],
                'name': r[12],
                'document_number': r[13],
                'rating': r[14],
                'phone': r[15]
            },
            'expiration_date': r[6],
            'status': r[7]
        }