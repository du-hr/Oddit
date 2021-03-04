from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username', 
            'password',
            'student_id',
            'club_name',
            'user_type'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        student_id = validated_data['student_id']
        user_type = validated_data['user_type']
        club_name = validated_data['club_name']
        user_obj = User(
            username = username,
            student_id = student_id,
            user_type = user_type,
            club_name = club_name
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj
