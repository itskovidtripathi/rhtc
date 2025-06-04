from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Event, Gallery

class EventListView(TemplateView):
    template_name = 'events/events.html'

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def gallery_list(request):
    galleries = Gallery.objects.all().order_by('-created_at')
    return render(request, 'events/gallery.html', {'galleries': galleries})
