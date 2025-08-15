# book/serializers.py
from rest_framework import serializers
from .models import BookProject

class BookProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProject
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

