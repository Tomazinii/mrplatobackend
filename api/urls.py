
from email.mime import base
from unicodedata import name
from django.urls import path,include,re_path
from rest_framework import routers

from .views import ApiAnswerView, ApiAskView, ApiContent, ApiNotification, ApiQuestionGameView, ApiTest, ListExerciseView, ListGameView,api_test,ApiQuestionExercise,ListChallengeView,ApiChallengeQuestion,TournammentGroup,TournammentMember,IntegrationMrplatoView,ExerciseListView

from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r"content",ApiContent)
router.register(r"ask",ApiAskView,basename="ask")
router.register(r"answer",ApiAnswerView,basename="answer")



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
    path("exercises/", ExerciseListView.as_view(), name="exercises")
]
