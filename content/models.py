from email.policy import default
from operator import mod
from django.db import models

from ckeditor.fields import RichTextField
# Create your models here.


class Content(models.Model):
    topic = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    text = RichTextField()
    slug = models.SlugField()
    created = models.DateField(auto_now=True)
    image = models.FileField(upload_to="content", blank=True, default="content/content.svg")


    def __str__(self):
        return self.topic


