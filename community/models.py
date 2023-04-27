from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

from infra.user.models import UserAccount

from ckeditor.fields import RichTextField



class Ask(models.Model):
	title = models.CharField(max_length=50)
	text = RichTextField()
	user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now=True)
	

	def get_answed(self,id):
		return Answer.objects.filter(pergunta=id)



	def __str__(self):
		return self.title
	

	class Meta:
		ordering = ['-created']



class Answer(models.Model):
	pergunta = models.ForeignKey(Ask, on_delete=models.CASCADE,related_name="resposta")
	text = models.TextField()
	image = models.FileField(upload_to=None, max_length=100,blank=True)
	user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.text
	


class ImageContent(models.Model):
	image = models.ImageField(blank=True)