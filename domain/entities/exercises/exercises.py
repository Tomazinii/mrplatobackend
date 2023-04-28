from domain.entities.objectValue import FileExercise, Slug

class Exercises:
    file: FileExercise
    slug: Slug
    list_name: str
    
    def __init__(self, file: FileExercise, slug: Slug, list_name: str):
        self.file = file
        self.slug = slug
        self.list_name = list_name

    @staticmethod
    def create(file: list, list_name: str):
        slug_objt = Slug.create(list_name)
        file_objt = FileExercise.create(file)

        if isinstance(slug_objt, Slug) and isinstance(file_objt, FileExercise):
            return Exercises(file=file_objt, slug=slug_objt, list_name=list_name)
        
        raise ValueError("Invalid Format")
