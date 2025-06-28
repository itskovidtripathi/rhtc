from django.contrib import admin
from .models import CareGiverProfile, UserRole
# Register your models here.



@admin.register(CareGiverProfile)
class CareGiverProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'designation', 'specialty', 'contact_number')
    search_fields = ('full_name', 'email', 'designation', 'specialty', 'contact_number')
    list_filter = ('designation', 'specialty')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)