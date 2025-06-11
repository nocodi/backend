from faker import Faker

import factory
from iam.models import IamUser

fake = Faker()


class IamUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IamUser

    email = factory.LazyAttribute(lambda x: fake.email())
    password = factory.LazyAttribute(lambda x: fake.password())
    created_at = factory.LazyFunction(fake.date_time)
    updated_at = factory.LazyFunction(fake.date_time)
