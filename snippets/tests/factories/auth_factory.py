import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

user = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = user

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    username = factory.Faker("user_name")
