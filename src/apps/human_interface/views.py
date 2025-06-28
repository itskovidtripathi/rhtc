from django.shortcuts import render

# Create your views here.

def list_care_givers(request):

    return render(request, 'human-interface/list_care_givers.html')