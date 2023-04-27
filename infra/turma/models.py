from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=50)
    start_period = models.DateField(auto_now=False, auto_now_add=False)
    end_period = models.DateField(auto_now=False, auto_now_add=False)
    
    def __str__(self) -> str:
        return self.name