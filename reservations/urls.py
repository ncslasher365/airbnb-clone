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
]
