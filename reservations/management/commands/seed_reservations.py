import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservations_models
from users import models as users_models
from rooms import models as rooms_models

NAME = "reservations"


class Command(BaseCommand):

    help = f"This command creates many {NAME} <3"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} you would like to create, bro :)",
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 2 - by default
        seeder = Seed.seeder()
        all_users = users_models.User.objects.all()
        all_rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(
                    ["pending", "confirmed", "cancelled"]
                ),
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created successfully!"))
