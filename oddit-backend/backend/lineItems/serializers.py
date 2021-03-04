from rest_framework import serializers
from .models import LineItem
from django.contrib.auth import get_user_model
import uuid

class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'

