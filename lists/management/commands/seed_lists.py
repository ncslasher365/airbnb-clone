import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as lists_models
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):

    help = "This command creates many lists <3"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many lists you would like to create, bro :)",
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 2 - by default
        seeder = Seed.seeder()
        all_users = users_models.User.objects.all()
        all_rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            lists_models.List,
            number,
            {
                "name": lambda x: seeder.faker.text(),
                "user": lambda x: random.choice(all_users),
            },
        )
        created_list = seeder.execute()
        created_clean = flatten(list(created_list.values()))
        for pk in created_clean:
            list_instance = lists_models.List.objects.get(pk=pk)
            to_add = all_rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_instance.places.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created successfully!"))
        # for pk in created_clean:
        #     list_instance = lists_models.List.objects.get(pk=pk)
        #     for room in all_rooms:
        #         magic_number = random.randint(2, 15)
        #         if magic_number % 2 == 0:
        #             list_instance.places.add(room)
        # if number > 1:
        #     self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
        # else:
        # self.stdout.write(self.style.SUCCESS(f"{number} list created!"))
