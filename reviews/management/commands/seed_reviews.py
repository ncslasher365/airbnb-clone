import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as reviews_models
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):

    help = "This command creates many reviews <3"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many reviews you would like to create, bro :)",
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 2 - by default
        seeder = Seed.seeder()
        all_users = users_models.User.objects.all()
        all_rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            reviews_models.Review,
            number,
            {
                "review": lambda x: seeder.faker.sentence(),
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "user": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            },
        )
        seeder.execute()
        if number > 1:
            self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"{number} review created!"))
