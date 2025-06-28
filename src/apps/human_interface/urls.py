from django.urls import path
from .views import list_care_givers, care_giver_profile, edit_care_giver_profile

app_name = 'human_interface'

urlpatterns = [
    path('care-givers/', list_care_givers, name='list_care_givers'),
    path('care-givers/<int:pk>/', care_giver_profile, name='care_giver_detail'),
    path('care-givers/edit/profile/', edit_care_giver_profile, name='edit_care_giver_profile'),
]
