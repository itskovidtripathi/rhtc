from django.db import models
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', args=[str(self.id)])

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
