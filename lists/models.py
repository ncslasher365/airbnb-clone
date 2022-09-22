from django.db import models
from core import models as core_models


# Create your models here.


class List(core_models.TimeStampedModel):

    """List Model Definition"""

    name = models.CharField(max_length=50)
    user = models.OneToOneField("users.User", related_name="list", on_delete=models.CASCADE)
    places = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_stays(self):
        return self.places.count()

    count_stays.short_description = "№ of rooms"
