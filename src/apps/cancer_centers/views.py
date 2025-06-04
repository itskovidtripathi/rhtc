from django.shortcuts import render
from .models import CancerCenter
from django.db.models import Q

def search(request):
    """Render the cancer center search form"""
    return render(request, 'cancer_centers/cancer-center-form.html')

def results(request):
    """Display cancer centers based on search criteria"""
    if request.method == 'GET':
        state = request.GET.get('state')
        city = request.GET.get('city')
        cancer_type = request.GET.get('cancer_type')

        # Start with all centers
        centers = CancerCenter.objects.all()

        # Apply filters if provided
        if state:
            centers = centers.filter(state=state)
        if city:
            centers = centers.filter(city__icontains=city)
        if cancer_type:
            centers = centers.filter(cancer_types__contains=[cancer_type])

        context = {
            'centers': centers,
            'state': state,
            'city': city,
            'cancer_type': cancer_type
        }
        
        return render(request, 'cancer_centers/show-cancer-centers.html', context)

    # If not GET, redirect to search form
    return render(request, 'cancer_centers/cancer-center-form.html')
