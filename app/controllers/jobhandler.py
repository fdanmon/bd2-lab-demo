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

    @classmethod
    def parse(cls, j):
        return {
            'id': j.id,
            'title': j.title,
            'description': j.description,
            'vacancies': j.vacancies,
            'category_id': j.category_id,
            'company_id': j.company_id,
            'expiration_date': j.expiration_date,
            'status': j.status
        }

    @classmethod
    def parse_job_appliances(cls, j):
        return {
            'person': {
                'id': j[0],
                'name': j[1],
                'rating': j[5]
            },
            'job': {
                'id': j[2],
                'name': j[3]
            },
            'appliance_date': j[4]
        }