from django.shortcuts import render, get_object_or_404
from .models import QuestionCategory, Question

def questions_category(request):
    categories = QuestionCategory.objects.all()
    return render(request, 'questions/questions-category.html', {'categories': categories})

def questions_list(request, category_slug):
    category = get_object_or_404(QuestionCategory, slug=category_slug)
    questions = Question.objects.filter(category=category)
    return render(request, 'questions/questions.html', {
        'category': category,
        'questions': questions,
    })

def resources(request):
    return render(request, 'questions/resources.html')
