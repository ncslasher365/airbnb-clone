from django.urls import path
from lists import views as lists_views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:room_pk>/", lists_views.toggle_room, name="toggle_room"),
    path("favs/", lists_views.SeeFavsView.as_view(), name="check_favs"),
]
