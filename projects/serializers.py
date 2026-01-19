from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

# User Serializer (optional for tasks/assignments)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Project name cannot be empty")
        return value



# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)  # optional nested info

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status',
            'due_date', 'project', 'assigned_to', 'created_at'
        ]


# User/Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)
        return user
