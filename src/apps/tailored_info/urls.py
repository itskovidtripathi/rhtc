from django.urls import path
from . import views

app_name = 'tailored_info'

urlpatterns = [
    path('options/', views.options, name='options'),
    path('options/details/', views.options_details, name='options_details'),
    path('supporters/', views.supporters, name='supporters'),
    path('esr/', views.esr_home, name='esr_home'),
    path('esr/early/', views.early_stage, name='early_stage'),
    path('esr/during/', views.during_stage, name='during_stage'),
    path('esr/after/', views.after_stage, name='after_stage'),
    path('schemes/', views.schemes, name='schemes'),
]
