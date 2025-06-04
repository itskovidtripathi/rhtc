from django.shortcuts import render

def options(request):
    return render(request, 'tailored_info/tailored-info-options.html')

def options_details(request):
    return render(request, 'tailored_info/tailored-info-options-details.html')

def supporters(request):
    return render(request, 'tailored_info/supporters.html')

def esr_home(request):
    return render(request, 'tailored_info/esr/esr.html')

def early_stage(request):
    return render(request, 'tailored_info/esr/early_stage.html')

def during_stage(request):
    return render(request, 'tailored_info/esr/during_stage.html')

def after_stage(request):
    return render(request, 'tailored_info/esr/after_stage.html')

def schemes(request):
    return render(request, 'tailored_info/government-schemes.html')