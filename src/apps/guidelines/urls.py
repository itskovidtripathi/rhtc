from django.urls import path
from . import views

app_name = 'guidelines'

urlpatterns = [
    path('', views.guideline_list, name='list'),
    path('lung/', views.lung_cancer_guidelines, name='lung'),
]