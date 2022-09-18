from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import ListView, DetailView, View, UpdateView
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django_countries import countries
from . import models as room_models, forms
from users import mixins as user_mixins


# Create your views here.


class HomeView(ListView):

    """HomeView Class Definition"""

    model = room_models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created"
    page_kwarg = "page"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """RoomDetail Class Definition"""

    model = room_models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(
                request.GET
            )  # UNBOUNDED FORM - INITIAL, BOUNDED - FILLED
            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("max_price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                bathrooms = form.cleaned_data.get("bathrooms")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if bedrooms is not None:
                    filter_args["bedrooms__exact"] = bedrooms

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bathrooms is not None:
                    filter_args["bathrooms__gte"] = bathrooms

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                query_set = room_models.Room.objects.filter(**filter_args).order_by(
                    "created",
                )

                paginator = Paginator(query_set, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                return render(
                    request,
                    "rooms/search.html",
                    {
                        "form": form,
                        "rooms": rooms,
                    },
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = room_models.Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "bathrooms",
        "check_in",
        "check_out",
        "instant_book",
        "house_rules",
        "amenities",
        "facilities",
    )
    template_name = "rooms/room_edit.html"

    def get_object(self, queryset=None):  # CHECKING FOR OBJECT EQUIVALENCE
        room = super().get_object(queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = room_models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = room_models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Sorry, can't delete that photo :(")
        else:
            room_models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(
                request, f"Photo {photo_pk} was succesfully deleted from room {room_pk}"
            )
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = room_models.Photo
    template_name = "rooms/photo_edit.html"
    fields = ("caption",)
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})
