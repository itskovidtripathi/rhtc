from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('faq/', views.faq, name='faq'),
    path('board/', views.board, name='board'),
    path('research/', views.research, name='research'),

]
