from django.db import models
from django.conf import settings
from apps.accounts.models import CareGiverProfile

# Create your models here.

class AppointmentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    caregiver = models.ForeignKey(CareGiverProfile, on_delete=models.CASCADE, related_name='appointments')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointment_requests')
    date_from = models.DateField()
    date_to = models.DateField()
    approved_date = models.DateField(blank=True, null=True)  # The date selected by caregiver
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.caregiver.full_name} by {self.requester.username} ({self.date_from} to {self.date_to})"
