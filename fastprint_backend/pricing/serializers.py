from rest_framework import serializers
from .models import *

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Dynamically assigned below
        fields = ['id', 'name', 'price']

def get_option_serializer(model_class):
    class OptionSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = [f.name for f in model_class._meta.fields if f.name in ['id', 'name', 'price']]
    return OptionSerializer