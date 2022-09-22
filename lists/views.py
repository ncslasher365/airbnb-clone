from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from lists import models as lists_models

# Create your views here.


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = lists_models.List.objects.get_or_create(
            user=request.user, name="My Favourite Houses"
        )
        if action == "add":
            the_list.places.add(room)
        elif action == "remove":
            the_list.places.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
