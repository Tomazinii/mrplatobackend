from domain.entities.objectValue import FileExercise, Slug

class Exercises:
    file: FileExercise
    slug: Slug
    list_name: str
    id: int
    
    def __init__(self, file: FileExercise, slug: Slug, list_name: str, id = None):
        self.file = file
        self.slug = slug
        self.list_name = list_name
        self.id = id

    @staticmethod
    def create(file: list, list_name: str, id: int = None):
        slug_objt = Slug.create(list_name)
        file_objt = FileExercise.create(file)

        if isinstance(slug_objt, Slug) and isinstance(file_objt, FileExercise):
            return Exercises(file=file_objt, slug=slug_objt, list_name=list_name, id=id)
        
        raise ValueError("Invalid Format")
