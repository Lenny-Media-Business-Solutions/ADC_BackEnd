from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    summary = models.TextField(help_text="Short summary for the news card")
    content = models.TextField(help_text="Full article content")
    image = CloudinaryField('news_image', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
