from django.contrib import admin
from .models import Guideline

@admin.register(Guideline)
class GuidelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'cancer_type', 'language')
    list_filter = ('cancer_type', 'language')
