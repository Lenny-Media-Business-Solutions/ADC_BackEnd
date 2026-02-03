from rest_framework import serializers
from .models import ImpactStory

class ImpactStorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImpactStory
        fields = ['id', 'title', 'slug', 'summary', 'content', 'image', 'image_url', 'published_date', 'is_featured']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
