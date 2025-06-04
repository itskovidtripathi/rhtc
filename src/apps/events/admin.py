from django.contrib import admin
from .models import Event, Gallery

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('date',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'created_at')
    list_filter = ('event',)
