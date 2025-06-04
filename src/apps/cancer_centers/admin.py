from django.contrib import admin
from .models import CancerCenter

@admin.register(CancerCenter)
class CancerCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'phone')
    list_filter = ('state', 'city')
    search_fields = ('name', 'address')
