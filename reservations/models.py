import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models
from . import managers

# Create your models here.


class BookedDay(models.Model):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


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
    objects = managers.CustomReservationManager()

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

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
