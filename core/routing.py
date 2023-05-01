from django.urls import path

from infra.tournamments.consumers import ChatConsumer,GroupTournamment

websocket_urlpatterns = [
    path("tournamment", ChatConsumer.as_asgi()),
    path("tournamment/<slug>",GroupTournamment.as_asgi()),
]