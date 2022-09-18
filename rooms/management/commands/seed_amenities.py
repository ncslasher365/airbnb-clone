from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates ameneties from the list in amenities variable"
    # print("Hello, Bro <3")

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you about love?"
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utinsils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free parking",
            "Free Wireless Connection",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Qveen size bed",
            "Restaraunt",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for amenity in amenities:
            Amenity.objects.create(name=amenity)
        self.stdout.write(self.style.SUCCESS("Amenities are created!"))
        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.SUCCESS("I love you"))
