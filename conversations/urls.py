from django.urls import path
from conversations import views as conversations_views

app_name = "conversations"

urlpatterns = [
    path(
        "go/<int:host_pk>/<int:guest_pk>/",
        conversations_views.GoConversationView,
        name="go_conversation",
    ),
    path(
        "<int:pk>/", conversations_views.ConversationDetailView.as_view(), name="detail"
    ),
]
