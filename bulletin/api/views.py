from rest_framework import generics

from bulletin.api.serializers import BulletinSerializer
from bulletin.models import Bulletin


class BulletinList(generics.ListAPIView):
    """Lists all bulletins in database."""
    serializer_class = BulletinSerializer
    queryset = Bulletin.objects.all()
