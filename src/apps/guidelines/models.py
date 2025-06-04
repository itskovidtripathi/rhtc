from django.db import models

class Guideline(models.Model):
    CANCER_TYPES = [
        ('lung', 'Lung Cancer'),
        ('breast', 'Breast Cancer'),
        ('oral', 'Oral Cancer'),
    ]
    
    LANGUAGES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
    ]

    title = models.CharField(max_length=255)
    cancer_type = models.CharField(max_length=50, choices=CANCER_TYPES)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    pdf_file = models.FileField(upload_to='guidelines/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"
