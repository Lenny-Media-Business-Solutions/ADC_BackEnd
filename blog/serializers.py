from rest_framework import serializers
from .models import News

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'summary', 'content', 'image', 'published_date', 'is_published')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation

class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'summary', 'content', 'image', 'published_date', 'is_published')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation
