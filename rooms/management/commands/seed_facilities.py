from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command creates facilities from the list in facilities variable"

    def handle(self, *args, **options):
        facilities = [
            "Private Entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for facility in facilities:
            Facility.objects.create(name=facility)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
