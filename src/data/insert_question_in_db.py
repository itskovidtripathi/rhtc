import os
import json
import django
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rare_and_hard_to_treat_cancers.settings')
django.setup()

# Use absolute import instead of relative
from apps.questions.models import QuestionCategory, Question

def create_categories():
    """Create question categories if they don't exist"""
    categories = {
        'risk': 'Risk Assessment Questions',
        'insurance': 'Insurance & Coverage Questions',
        'screening': 'Screening Process Questions',
        'test_results': 'Test Results Questions',
        'biopsies': 'Biopsy Questions',
    }
    
    category_objects = {}
    for slug, name in categories.items():
        category, created = QuestionCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': f'Common questions about {name.lower()}'
            }
        )
        category_objects[slug] = category
        print(f"{'Created' if created else 'Found'} category: {name}")
    
    return category_objects

def load_questions(json_file):
    """Load questions from JSON file"""
    with open(json_file, 'r') as f:
        return json.load(f)

def insert_questions(questions_data, categories):
    """Insert questions into database"""
    for category_slug, questions in questions_data.items():
        category = categories.get(category_slug)
        if not category:
            print(f"Warning: Category {category_slug} not found")
            continue
            
        for q_data in questions:
            question, created = Question.objects.get_or_create(
                category=category,
                question=q_data['question'],
                defaults={'answer': q_data['answer']}
            )
            if created:
                print(f"Added question: {q_data['question'][:50]}...")
            else:
                print(f"Updated question: {q_data['question'][:50]}...")

def main():
    try:
        print("Starting question import process...")
        
        # Create categories
        categories = create_categories()
        
        # Load questions from JSON
        json_file = os.path.join(os.path.dirname(__file__), 'lung_cancer_questions_with_answers.json')
        questions_data = load_questions(json_file)
        
        # Insert questions
        insert_questions(questions_data, categories)
        
        print("\nImport completed successfully!")
        
    except Exception as e:
        print(f"Error during import: {str(e)}")
        raise

if __name__ == '__main__':
    main()
