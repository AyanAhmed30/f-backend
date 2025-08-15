from rest_framework import serializers
from .models import *

class BindingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingType
        fields = '__all__'

class SpineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spine
        fields = '__all__'

class ExteriorColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExteriorColor
        fields = '__all__'

class FoilStampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoilStamping
        fields = '__all__'

class ScreenStampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenStamping
        fields = '__all__'

class CornerProtectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CornerProtector
        fields = '__all__'

class InteriorColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorColor
        fields = '__all__'

class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperType
        fields = '__all__'

class TrimSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrimSize
        fields = '__all__'
