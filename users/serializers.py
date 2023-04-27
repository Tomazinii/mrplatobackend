from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers

from infra.user.models import PhotoUser

class UserCreateSerializer(UserCreateSerializer):
    photo = serializers.SerializerMethodField("get_image")

    def get_image(self,obj):
        print("TESTE",obj.id)

        photo = PhotoUser.objects.filter(user=obj.id)[0]
        return str(photo.photo)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password','photo',"matriculation",'nickname',"score_user")


class UserSerializerView(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("photo","username","id","nickname","matriculation","score_user")
