import factory
from faker import Faker

from bot.models import Bot

fake = Faker()


class BotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bot

    name = factory.Sequence(lambda n: fake.name())
    description = factory.LazyAttribute(lambda x: fake.text())
    token = factory.Sequence(lambda n: fake.name())
    user = factory.SubFactory("iam.test.factory.IamUserFactory")
    created_at = factory.LazyFunction(fake.date_time)
    updated_at = factory.LazyFunction(fake.date_time)
