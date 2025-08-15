from rest_framework import serializers
from .models import *

class TrimSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrimSize
        fields = '__all__'

class BindingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingType
        fields = '__all__'

class InteriorColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorColor
        fields = '__all__'

class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperType
        fields = '__all__'

class CoverFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverFinish
        fields = '__all__'


