from django.contrib import admin
from .models import AppointmentRequest

# Register your models here.
@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('caregiver', 'requester', 'date_from', 'date_to', 'status', 'created_at')
    search_fields = ('caregiver__full_name', 'requester__username')
    list_filter = ('status',)
