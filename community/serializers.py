from infra.user.models import PhotoUser,UserAccount
from rest_framework import serializers
from .models import Ask,Answer,ImageContent

class AskSerializer(serializers.ModelSerializer):
	resposta = serializers.SerializerMethodField("get_resposta")
	name = serializers.SerializerMethodField("get_test")
	image = serializers.SerializerMethodField("get_image")
	
	def get_image(self,obj):

		photo = PhotoUser.objects.filter(user=obj.user.id)[0]
		return str(photo.photo)

		
	def get_test(self,obj):
		user = UserAccount.objects.filter(id=obj.user.id)[0]
		return user.nickname

	def get_resposta(self,obj):
		p = Ask()
		return len(p.get_answed(obj.pk))
	class Meta:
		model = Ask 
		fields = "__all__"

class AnswerSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField("get_username")
	image = serializers.SerializerMethodField("get_image")
	
	def get_image(self,obj):

		photo = PhotoUser.objects.filter(user=obj.user.id)[0]
		return str(photo.photo)

	def get_username(self,obj):
		return obj.user.nickname
	class Meta:
		model = Answer 
		fields = "__all__"



class ImageContentSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = ImageContent 
		fields = "__all__"