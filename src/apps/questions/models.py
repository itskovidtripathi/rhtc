from django.db import models

class QuestionCategory(models.Model):
    CATEGORY_CHOICES = [
        ('risk', 'Risk Assessment'),
        ('insurance', 'Insurance & Coverage'),
        ('screening', 'Screening Process'),
        ('test_results', 'Test Results'),
        ('biopsies', 'Biopsy'),
    ]

    name = models.CharField(max_length=100)
    slug = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        unique=True,
        default='risk'  # Adding default value
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Question Categories"

class Question(models.Model):
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:100]
