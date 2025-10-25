import factory
from factory.django import DjangoModelFactory
from snippets.models import Snippet, Tag

from .auth_factory import UserFactory


class SnippetFactory(DjangoModelFactory):
    class Meta:
        model = Snippet

    title = factory.Faker("sentence", nb_words=4)
    note = factory.Faker("paragraph", nb_sentences=3)
    created_by = factory.SubFactory(UserFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.Faker("word")
