from django.urls import path
from .views import list_care_givers

app_name = 'human_interface'

urlpatterns = [
    path('care-givers/', list_care_givers, name='list_care_givers'),
]
