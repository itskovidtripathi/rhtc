from django.urls import path
from . import views

app_name = 'cancer_centers'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('results/', views.results, name='results'),
]
