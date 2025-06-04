from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('category/', views.questions_category, name='category'),
    path('list/<str:category_slug>/', views.questions_list, name='list'),
    path('resources/', views.resources, name='resources'),
]
