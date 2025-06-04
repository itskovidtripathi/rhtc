from django.contrib import admin
from .models import QuestionCategory, Question

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
