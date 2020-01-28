from rest_framework import serializers

from bulletin.models import Bulletin


class BulletinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bulletin
        exclude = ['id']
