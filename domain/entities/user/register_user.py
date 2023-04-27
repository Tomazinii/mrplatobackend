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
            return RegisterUser(obj_file, Class)
        return ValueError("Invalid File")
    
    def transform(self, file):

        """transform list data in list with dicts

        Args:
            file (_type_): _description_

        Returns:
            _type_: _description_
        """

        result_list = []

        for line in file:
            datas = line.split("-")
            username = datas[1].strip()
            matriculation = datas[2].strip()
            email = datas[3].strip()
            dict_line = {"username": username, "matriculation": matriculation, "email": email}
            result_list.append(dict_line)
        
        return result_list

    
    def get_data(self) -> list:
        result = self.transform(self.file.get_file())
        return result
        