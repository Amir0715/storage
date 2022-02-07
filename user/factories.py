import factory
from factory.django import DjangoModelFactory

from user.models import User, City

class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker('city', locale='ru_RU')

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    other_name = factory.Faker('middle_name', locale='ru_RU')
    phone = factory.Faker('phone_number')
    birthday = factory.Faker('past_date')
    city = factory.SubFactory(CityFactory)
    additional_info = factory.Faker('sentence', nb_words=10, variable_nb_words=True, locale='ru_RU')