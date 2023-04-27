from interfaces.repository import ClassRepository as ClassRepositoryInterface
from .models import Class

class ClassRepository(ClassRepositoryInterface):

    @classmethod
    def find(self, id: int):
        try:
            turma = Class.objects.filter(id=id)
            return turma
        except: 
            raise Exception("find Class error")
        
    @classmethod
    def update(self):
        return super().update()
    
    @classmethod
    def create(self, id, name, teacher_id, start, end):
        return super().create(id, name, teacher_id, start, end)