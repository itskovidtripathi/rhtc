from django.db import models

class CancerHospitals(models.Model):
    host_code = models.CharField(max_length=255)
    hospital = models.CharField(max_length=255)
    center = models.CharField(max_length=255)
    pin_code = models.IntegerField()
    geo_location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone_tel = models.BigIntegerField()
    website = models.CharField(max_length=255)
    review = models.FloatField(max_length=255)
    review_count = models.IntegerField()
    wheelchair = models.CharField(max_length=255)
    blood_bank = models.CharField(max_length=255)
    pathology = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    coords = models.CharField(max_length=255)
    hospital_policy = models.CharField(max_length=255, null=True, blank=True)
    palliative_care = models.CharField(max_length=25, null=True, blank=True)
    diagnosis_center = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.hospital
