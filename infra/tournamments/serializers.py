from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Group,Members


class GroupSerializer(ModelSerializer):
    number = serializers.SerializerMethodField("get_member")

    def get_member(self,obj):
        member = Members.objects.filter(group=obj).__len__()
        return member

    class Meta:
        model = Group
        fields = ["name","slug","number"]
        
class MemberSerializer(ModelSerializer):
    username = serializers.SerializerMethodField("get_name")
    email = serializers.SerializerMethodField("get_email")


    def get_email(self,obj):
        return obj.user.email

    def get_name(self,obj):
        return obj.user.username


    class Meta:
        model = Members
        fields = "__all__"
