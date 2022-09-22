from django.urls import path
from reservations import views as reservation_views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>/",
        reservation_views.CreateReservation,
        name="create_reservation",
    ),
    path("<int:pk>/", reservation_views.ReservationDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/<str:verb>",
        reservation_views.EditReservationView,
        name="edit_reservation",
    ),
    path(
        "list/",
        reservation_views.ReservationsListView.as_view(),
        name="view_reservation",
    ),
]
