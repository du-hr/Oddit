from rest_framework import serializers
from events.models import Event
from django.contrib.auth import get_user_model
import uuid

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

