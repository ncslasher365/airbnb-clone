from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import forms
from rooms import models as room_models

# Create your views here.


def CreateReview(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(
            request.POST
        )  # GET DATA FROM THE FORM BY GIVING REQUEST.POST AS AN ARGUMENT
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room succesfully reviewed!")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
        else:
            messages.error(request, "Sorry, there is no way to post the review :(")
            return redirect(reverse("core:home"))
