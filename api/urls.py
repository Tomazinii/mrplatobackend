
from email.mime import base
from unicodedata import name
from django.urls import path,include,re_path
from rest_framework import routers

from .views import ApiAnswerView, ApiAskView, ApiContent, ApiNotification, ApiQuestionGameView, ApiTest, ListExerciseView, ListGameView,api_test,ApiQuestionExercise,ListChallengeView,ApiChallengeQuestion,TournammentGroup,TournammentMember,IntegrationMrplatoView,ExerciseListView

from rest_framework.routers import SimpleRouter

from .views import GroupsView,MembersView

router = SimpleRouter()

router.register(r"content",ApiContent)
router.register(r"ask",ApiAskView,basename="ask")
router.register(r"answer",ApiAnswerView,basename="answer")


from rest_framework_simplejwt import views
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request

class MyCustomRequest(Request):
    def __init__(self, some_custom_data=None, *args, **kwargs):
        self.some_custom_data = some_custom_data
        super(MyCustomRequest, self).__init__(*args, **kwargs)

    def parse(self, stream, media_type=None, parser_context=None):
        # Aqui você pode adicionar a lógica de parsing personalizada para a sua request
        # baseada nos dados do stream, tipo de mídia, e contexto do parser
        # Exemplo básico de parsing que apenas verifica se o valor do campo 'custom_data'
        # é igual ao valor fornecido em 'some_custom_data'
        data = super(MyCustomRequest, self).parse(stream, media_type, parser_context)
        if 'custom_data' in data and data['custom_data'] != self.some_custom_data:
            raise Exception("Valor inválido para custom_data")
        return data

from django.http import QueryDict

class AuthenticationService(views.TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        data = {
            'csrfmiddlewaretoken': ['VdApOYE1kH0ZcxB5bb51annkfRAj0sZBfD5ZJIMSG1IDC6KtwIZ82eXEGAkLz7Fn'],
            'email': ['a@a.com'],
            'password': ['123']
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        
        return super().post(query_dict, *args, **kwargs)




urlpatterns = [
    path("",include(router.urls)),
    path("notification/",ApiNotification.as_view(),name="notification"),
    path("list-exercise/",ListExerciseView.as_view({"get":"list"}),name="list"),
    re_path("list-exercise/question/(?P<id>.+)/$",ApiQuestionExercise.as_view(),name="exercise"),
    path("list-challenge/",ListChallengeView.as_view(),name="list-challenge"),
    re_path("list-challenge/question/(?P<id>.+)/$",ApiChallengeQuestion.as_view(),name="challenge"),
    path("list-game/",ListGameView.as_view(),name="list-game"),
    path("list-game-question/",ApiQuestionGameView.as_view(),name="list-game-question"),
    path("tournamment-group/",TournammentGroup.as_view({"get":"list"})),
    path("tournamment-member/",TournammentMember.as_view({"get":"list"})),
    path("mrplato/", IntegrationMrplatoView.as_view(), name="mrplato"),
    path("exercises/", ExerciseListView.as_view(), name="exercises"),
    path("groups/",GroupsView.as_view(), name="groups"),
    path("members/", MembersView.as_view(), name="members")
]
