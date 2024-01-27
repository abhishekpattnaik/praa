# from django.contrib.auth.models import Group, User
from data_pull.models import Record
from rest_framework import serializers


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
