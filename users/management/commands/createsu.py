from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser <3"

    def handle(self, *args, **options):

        admin = User.objects.get(username="ebadmin")
        if not admin:
            User.objects.create_superuser(
                "ebadmin", "nikita.tsepochko20@gmail.com", "123nomad123"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser exists!"))
