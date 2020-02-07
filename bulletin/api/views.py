from rest_framework import generics

from bulletin.api.serializers import BulletinSerializer
from bulletin.models import Bulletin


class BulletinList(generics.ListAPIView):
    """Lists all bulletins in database.

    But excludes items with null `time_of_quake` field.
    """
    serializer_class = BulletinSerializer
    queryset = Bulletin.objects.exclude(time_of_quake=None).all()
