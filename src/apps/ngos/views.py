from django.shortcuts import render, get_object_or_404
from .models import NGO

def ngo_list(request):
    ngos = NGO.objects.all().order_by('name')
    return render(request, 'ngos/ngo_list.html', {'ngos': ngos})

def ngo_detail(request, pk):
    ngo = get_object_or_404(NGO, pk=pk)
    return render(request, 'ngos/ngo_details.html', {'ngo': ngo})
