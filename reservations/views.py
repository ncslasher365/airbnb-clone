import datetime
from django.http import Http404
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect, reverse
from users import mixins as user_mixins
from django.contrib import messages
from rooms import models as room_models
from reviews import forms as review_forms
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
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def EditReservationView(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.room.host != request.user and reservation.guest != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELLED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation was updated :)")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationsListView(TemplateView):

    template_name = "reservations/reservations_list.html"
