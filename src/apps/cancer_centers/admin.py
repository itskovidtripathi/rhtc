from django.contrib import admin
from .models import CancerHospitals

@admin.register(CancerHospitals)
class CancerHospitalsAdmin(admin.ModelAdmin):
    list_display = ['host_code', 'hospital', 'city', 'region', 'country', 'phone_tel', 'review', 'blood_bank', 'pathology']
    list_filter = ['country', 'region', 'city', 'blood_bank', 'pathology']
    search_fields = ['hospital', 'city', 'country', 'tags']
    list_per_page = 20