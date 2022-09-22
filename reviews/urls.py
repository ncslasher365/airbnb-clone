from django.urls import path
from reviews import views as reviews_views

app_name = "reviews"

urlpatterns = [
    path("create/<int:room>", reviews_views.CreateReview, name="create"),
]
