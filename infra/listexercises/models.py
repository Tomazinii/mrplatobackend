from django.db import models


class ListExerciseModel(models.Model):
    file = models.FileField(upload_to=None, max_length=255)
    list_name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Add List Exercises'
    def __str__(self) -> str:
        return f"{self.list_name}"
