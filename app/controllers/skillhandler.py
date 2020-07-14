class SkillHandler(object):
    def __init__(self):
        pass
    
    @classmethod
    def parse_info(cls, s):
        return {
            'id': s.id,
            'title': s.title,
            'category_id': s.category_id
        }
