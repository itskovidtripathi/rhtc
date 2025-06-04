from django.urls import path
from .views import EventListView, GalleryView

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
]