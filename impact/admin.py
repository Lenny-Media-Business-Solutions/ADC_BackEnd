from django.contrib import admin
from .models import ImpactStory

@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_featured')
    list_filter = ('is_featured', 'published_date')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
