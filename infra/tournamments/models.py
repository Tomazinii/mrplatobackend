from django.db import models

from infra.user.models import UserAccount

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField()
    turma = models.ForeignKey("turma.Class", on_delete=models.CASCADE)
    pin = models.CharField(max_length=10,blank=True)

    def __str__(self) -> str:
        return self.name

class Members(models.Model):
    boss = models.BooleanField(default=False)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.group.id}"

