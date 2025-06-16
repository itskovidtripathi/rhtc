from django.db import models

class NGO(models.Model):
    name = models.CharField(max_length=200)
    founded_by = models.CharField(max_length=200)
    founded_year = models.IntegerField(null=True, blank=True)
    coverage = models.CharField(max_length=500)
    services = models.JSONField()  # Store list of services
    description = models.TextField()
    remarks = models.TextField()
    website = models.URLField()

    # Contact Information
    contact_info = models.JSONField()  # Store phone and email as JSON
    
    # Social Media Links
    social_media = models.JSONField()  # Store social media links as JSON

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NGO"
        verbose_name_plural = "NGOs"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_services_list(self):
        return self.services if isinstance(self.services, list) else []

    def get_contact_phones(self):
        return self.contact_info.get('phone', []) if isinstance(self.contact_info, dict) else []

    def get_contact_emails(self):
        return self.contact_info.get('email', []) if isinstance(self.contact_info, dict) else []

    def get_social_media_links(self):
        return self.social_media if isinstance(self.social_media, dict) else {}
