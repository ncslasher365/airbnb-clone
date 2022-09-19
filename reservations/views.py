import datetime
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from users import mixins as user_mixins
from django.contrib import messages
from rooms import models as room_models
from . import models

# Create your views here.


class CreateError(Exception):
    pass


def CreateReservation(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Sorry, can not create the reservation :(")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(user_mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation and (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation}
        )
