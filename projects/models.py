from django.db import models
from programs.models import Program

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects')
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
