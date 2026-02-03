from django.db import models
from programs.models import Program

class PartnershipInquiry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='partnership_inquiries')
    organization_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    partnership_type = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization_name} - {self.program.title}"
