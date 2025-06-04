from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def profile(request):
    return render(request, 'core/profile.html')

def faq(request):
    return render(request, 'core/faq.html')

def board(request):
    return render(request, 'core/board.html')

def research(request):
    return render(request, 'core/research.html')

