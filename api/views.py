from urllib import request
from django.shortcuts import render
from community.models import Ask,Answer
from api.serializers import ContentSerializer,NotificationSerializer
from content.models import Content
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework import status
from notification.models import Notification
import json
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status
from exercises.serializers import ListExerciseSerializer,QuestionExerciseSerializer,ListChallengeSerializer,QuestionChallengeSerializer
from exercises.models import ListExercise,Question,ListChallenge,QuestionChallenge
from community.serializers import AskSerializer,AnswerSerializer
from games.models import QuestionGame,ListQuestionGame
from games.serializers import ListGameSerializer,QuestionGameSerializer

from tournamment.serializers import GroupSerializer,MemberSerializer
from tournamment.models import Members,Group


from community.permissions import isTestOrReadOnly


class ApiTest(APIView):
	def get(self,request):
		return Response({"okokokokok"})

	def post(self,request):
		print("DASDsadsasadad",request.data)
		return Response(request.data,status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET','POST'])
def api_test(request):
    return Response({"message":"okokok"})



class ApiContent(ModelViewSet):
	queryset = Content.objects.using("mrplatofixed").all()
	serializer_class = ContentSerializer

	def create(self, request, *args, **kwargs):
		return Response("Unauthorized",status=status.HTTP_401_UNAUTHORIZED)

	def destroy(self, request, *args, **kwargs):
		return Response("Unauthorized",status=status.HTTP_401_UNAUTHORIZED)

	def update(self, request, *args, **kwargs):
		return Response("Unauthorized",status=status.HTTP_401_UNAUTHORIZED)


class ApiNotification(ListAPIView):
	queryset = Notification.objects.using("mrplatofixed").all()
	serializer_class = NotificationSerializer




class ListExerciseView(ModelViewSet):
	queryset = ListExercise.objects.using("mrplatofixed").all()
	serializer_class = ListExerciseSerializer


class ApiQuestionExercise(ListAPIView):
	serializer_class = QuestionExerciseSerializer
	def get_queryset(self):
		query = Question.objects.filter(list=self.kwargs["id"])
		return query

class ListChallengeView(ListAPIView):
	serializer_class = ListChallengeSerializer
	queryset = ListChallenge.objects.using("mrplatofixed").all()

class ApiChallengeQuestion(ListAPIView):
	serializer_class = QuestionChallengeSerializer
	def get_queryset(self):
		query = QuestionChallenge.objects.filter(list=self.kwargs["id"])
		return query

class ApiAskView(ModelViewSet):
	permission_classes = [isTestOrReadOnly,]
	serializer_class = AskSerializer
	queryset = Ask.objects.all()


class ApiAnswerView(ModelViewSet):
	permission_classes = [isTestOrReadOnly]
	serializer_class = AnswerSerializer
	
	def get_queryset(self):
		id = self.request.GET.get("ask")
		queryset = Answer.objects.filter(pergunta=id)
		return queryset
		



class ListGameView(ListAPIView):
	queryset = ListQuestionGame.objects.filter(availability=True)
	serializer_class = ListGameSerializer


class ApiQuestionGameView(ListAPIView):
	serializer_class = QuestionGameSerializer

	def get_queryset(self):
		id = self.request.GET.get("list")
		queryset = QuestionGame.objects.filter(list=id)
		return queryset


class TournammentGroup(ModelViewSet):
	serializer_class = GroupSerializer
	queryset =  Group.objects.all()


from users.utils import score

class TournammentMember(ModelViewSet):
	serializer_class = MemberSerializer
	queryset =  Members.objects.all()

	def get_queryset(self):
		score(type="exercises",question_id=2, user=self.request.user,time=0,attempet=0)
		score(type="exercises",question_id=1, user=self.request.user,time=0,attempet=0)
		score(type="challenges",question_id=2, user=self.request.user,time=0,attempet=0)
		score(type="tournamment",question_id=2, user=self.request.user,time=0,attempet=0)
		score(type="games",question_id=2, user=self.request.user,time=0,attempet=0)
		return super().get_queryset()
	

from adapter import django_adapter
from composer import integration_mrplato_composite, get_list_exercise_composite

class IntegrationMrplatoView(APIView):
	def get(self,request):
		return Response({"okokokokok"})

	def post(self,request):
		response = django_adapter(request=request, api_route=integration_mrplato_composite())
		return Response(response.body,status=response.status_code)


class ExerciseListView(APIView):
	""" this is class exercise view """

	def get(self, request):
		response = django_adapter(request=request, api_route=get_list_exercise_composite())
		return Response(response.body, response.status_code)