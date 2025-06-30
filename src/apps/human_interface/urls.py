from django.urls import path
from .views import (
    list_care_givers,
    care_giver_profile,
    edit_care_giver_profile,
    schedule_appointment,
    check_appointment_requests,
    appointment_status_view,
)

app_name = 'human_interface'

urlpatterns = [
    path('care-givers/', list_care_givers, name='list_care_givers'),
    path('care-givers/<int:pk>/', care_giver_profile, name='care_giver_detail'),
    path('care-givers/edit/profile/', edit_care_giver_profile, name='edit_care_giver_profile'),
    path('care-givers/<int:caregiver_id>/schedule-appointment/', schedule_appointment, name='schedule_appointment'),
    path('care-givers/check-appointments/', check_appointment_requests, name='care_giver_appointments'),
    path('appointments/status/', appointment_status_view, name='appointment_status'),
]
