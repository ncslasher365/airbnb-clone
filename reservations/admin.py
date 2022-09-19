from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "room",
        "check_in",
        "check_out",
        "status",
        "guest",
        "is_in_progress",
        "is_finished",
    )

    list_filter = ("status",)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    list_display = ("day", "reservation", "created", "updated")
