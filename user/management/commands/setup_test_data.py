import random
from django.db import transaction
from django.core.management.base import BaseCommand

from user.models import User, City
from user.factories import UserFactory, CityFactory

NUM_USERS = 200
NUM_CITIES = 20

class Command(BaseCommand):
    help = "Generate test data"

    def add_arguments(self, parser) -> None:
        parser.add_argument('-u', '--users', type=int, help='Number of users', default=NUM_USERS)
        parser.add_argument('-c', '--cities', type=int, help='Number of cities', default=NUM_CITIES)


    @transaction.atomic
    def handle(self, *args, **kwargs):
        num_users = kwargs.get('users', NUM_USERS)
        num_cities = kwargs.get('cities', NUM_CITIES)

        self.stdout.write("Deleting old data...")
        models = [User, City]
        for m in models: 
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        cities = []
        for _ in range(num_cities):
            cities.append(CityFactory())

        users = []
        for _ in range(num_users):
            city = random.choice(cities)
            users.append(UserFactory(city=city))

        self.stdout.write(f"{num_users} users and {num_cities} was created.")
