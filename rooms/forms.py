from django import forms
from django_countries.fields import CountryField
from . import models as room_models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")  # RENDER A WIDGET
    country = CountryField(default="UA").formfield()
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind of rooms",
        queryset=room_models.RoomType.objects.all(),
    )
    max_price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False, max_value=15)
    bathrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=room_models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=room_models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
