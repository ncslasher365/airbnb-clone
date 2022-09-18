from re import L
from django.db import models
from django.utils import timezone
from core import models as core_models

# Create your models here.


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=15, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} - {self.guest}"

    def is_in_progress(self):
        now = timezone.now().date()
        # if now > self.check_in and now < self.check_out:
        #     print("Reservation is in progress")
        return now >= self.check_in and now <= self.check_out

    is_in_progress.boolean = True
    is_in_progress.short_description = "Reservation in progress"

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
    is_finished.short_description = "Reservation finished"
