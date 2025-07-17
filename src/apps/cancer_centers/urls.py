from django.urls import path
from .views import Index, search_hospitals

app_name = 'cancer_centers'

urlpatterns = [
    path('CancerCareLocator/', Index, name='hospital_locator'),
    path('search/', search_hospitals, name='search'),
]
