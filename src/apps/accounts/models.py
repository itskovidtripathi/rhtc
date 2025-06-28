from django.db import models
from django.contrib.auth.models import User

# For custom user fields, create a Profile model linked to User if needed.

class CareGiverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caregiver_profile')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)  # New mandatory field
    designation = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='caregivers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    contact_number = models.CharField(max_length=20, blank=True)  # Will be set to WhatsApp/mobile at signup
    # Social profile links
    social_linked_in = models.URLField("LinkedIn Profile", blank=True, null=True)
    social_twitter = models.URLField("Twitter Profile", blank=True, null=True)
    social_facebook = models.URLField("Facebook Profile", blank=True, null=True)
    # Add other relevant fields as needed

    def save(self, *args, **kwargs):
        # Ensure contact_number is always equal to the user's username (whatsapp/mobile)
        if self.user and self.user.username:
            self.contact_number = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
