from django.db import models

class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True)
    area_of_interest = models.CharField(max_length=255)
    availability = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    motivation = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.area_of_interest}"
