from datetime import timedelta
import random

from django.utils import timezone
import factory


class BulletinFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'bulletin.Bulletin'

    url = factory.Sequence(lambda n: f'https://www.sitepage.com/{n}')
    latitude = factory.Faker(
        'pydecimal',
        right_digits=2,
        min_value=-90,
        max_value=90
    )
    longitude = factory.Faker(
        'pydecimal',
        right_digits=2,
        min_value=-180,
        max_value=180
    )
    depth = factory.Faker(
        'pydecimal',
        right_digits=1,
        min_value=0,
        max_value=500
    )
    magnitude = factory.Faker(
        'pydecimal',
        right_digits=1,
        min_value=1,
        max_value=10
    )
    location = factory.Faker('address')

    @factory.sequence
    def time_of_quake(n):
        """Creates sequence of datetime obj 30 minutes apart."""
        td = timedelta(minutes=30)
        return timezone.now() - (n * td)
