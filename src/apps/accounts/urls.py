from django.urls import path
from .views import login_view, signup_view, logout_view, caregiver_login_view, caregiver_signup_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('caregiver/signup/', caregiver_signup_view, name='caregiver_signup'),
    path('caregiver/login/', caregiver_login_view, name='caregiver_login'),
]
