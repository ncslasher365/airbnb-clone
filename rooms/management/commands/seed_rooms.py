import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as rooms_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many users <3"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms you would like to create, bro :)",
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 2 - by default
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = rooms_models.RoomType.objects.all()
        amenities = rooms_models.Amenity.objects.all()
        house_rules = rooms_models.HouseRule.objects.all()
        facilities = rooms_models.Facility.objects.all()
        seeder.add_entity(
            rooms_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(25, 250),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "bathrooms": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 10),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        print(created_clean)
        for pk in created_clean:
            room = rooms_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                rooms_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(2, 30)}.webp",
                )
            for amenity in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)
            for facility in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)
            if house_rules.count() != 0:
                for house_rule in house_rules:
                    magic_number = random.randint(0, 15)
                    if magic_number % 2 == 0:
                        room.house_rules.add(house_rule)

        self.stdout.write(
            self.style.SUCCESS(
                f"{number} rooms created, used {all_users.count()} users"
            )
        )
