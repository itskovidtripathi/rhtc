from django.db import models

class CancerCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True)
    cancer_types = models.JSONField()  # Store supported cancer types
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
