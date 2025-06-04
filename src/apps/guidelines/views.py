from django.shortcuts import render
from .models import Guideline

def guideline_list(request):
    guidelines = Guideline.objects.all().order_by('cancer_type')
    return render(request, 'guidelines/guidelines.html', {
        'guidelines': guidelines
    })

def lung_cancer_guidelines(request):
    return render(request, 'guidelines/lung-cancer-guidelines.html')
