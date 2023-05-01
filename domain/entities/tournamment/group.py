from domain.entities.objectValue import Slug

class Group:
    turma: int
    name: str
    slug: Slug
    
    def __init__(self, turma, name, slug):
        self.turma = turma
        self.name = name
        self.slug = slug

    @staticmethod
    def create(turma: int, name: str):
        obj_slug = Slug.create(name)
        if isinstance(obj_slug, Slug):
            return Group(turma, name, obj_slug)