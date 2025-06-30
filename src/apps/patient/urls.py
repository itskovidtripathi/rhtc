from django.urls import path
from .views import patient_profile_view

app_name = 'patient'

urlpatterns = [
    path('profile/', patient_profile_view, name='profile'),
]
