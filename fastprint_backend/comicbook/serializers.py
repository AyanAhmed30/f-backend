from rest_framework import serializers
from .models import (
    ComicTrimSize,
    ComicInteriorColor,
    ComicPaperType,
    ComicCoverFinish,
    ComicBindingType,
)


class ComicTrimSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicTrimSize
        fields = ['id', 'name']

class ComicBindingTypeSerializer(serializers.ModelSerializer):
    trim_size = ComicTrimSizeSerializer(read_only=True)

    class Meta:
        model = ComicBindingType
        fields = ['id', 'name', 'price', 'min_pages', 'max_pages', 'trim_size']

class ComicInteriorColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicInteriorColor
        fields = '__all__'


class ComicPaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicPaperType
        fields = '__all__'


class ComicCoverFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicCoverFinish
        fields = '__all__'


class ComicBindingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicBindingType
        fields = '__all__'
