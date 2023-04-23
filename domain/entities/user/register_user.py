from domain.entities.objectValue import File

class RegisterUser:
    file: File
    Class: int

    def __init__(self, file: File, Class):
        self.file = file
        self.Class = Class

    @staticmethod
    def create(file: list, Class):
        obj_file = File.create(file)
        if isinstance(obj_file, File) and isinstance(Class, int):
            return RegisterUser(file, Class)
        return ValueError("Invalid File")