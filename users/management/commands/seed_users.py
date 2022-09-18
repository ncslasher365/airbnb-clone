from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates many users <3"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users you would like to create, bro :)",
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 2 - by default
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
