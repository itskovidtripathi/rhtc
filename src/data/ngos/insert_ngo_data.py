import os
import json
import django
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rare_and_hard_to_treat_cancers.settings')
django.setup()

from apps.ngos.models import NGO

def load_ngo_data(json_file):
    """Load NGO data from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_ngos(ngos_data):
    """Insert NGOs into database"""
    for ngo_data in ngos_data:
        try:
            # Try to get existing NGO or create new one
            ngo, created = NGO.objects.get_or_create(
                name=ngo_data['name'],
                defaults={
                    'founded_by': ngo_data['founded_by'],
                    'founded_year': ngo_data.get('founded_year'),  # using get() for optional fields
                    'coverage': ngo_data['coverage'],
                    'services': ngo_data['services'],
                    'contact_info': ngo_data['contact_info'],
                    'website': ngo_data['website'],
                    'social_media': ngo_data['social_media'],
                    'remarks': ngo_data['remarks'],
                    'description': ngo_data['description']
                }
            )

            if created:
                print(f"Created new NGO: {ngo.name}")
            else:
                # Update existing NGO
                for key, value in ngo_data.items():
                    if key != 'name':  # Skip the name field
                        setattr(ngo, key, value)
                ngo.save()
                print(f"Updated existing NGO: {ngo.name}")

        except Exception as e:
            print(f"Error processing NGO {ngo_data.get('name', 'Unknown')}: {str(e)}")

def main():
    try:
        print("Starting NGO data import process...")
        
        # Get path to JSON file
        json_file = os.path.join(os.path.dirname(__file__), 'ngos_info.json')
        
        # Load and validate data
        ngos_data = load_ngo_data(json_file)
        print(f"Loaded {len(ngos_data)} NGOs from JSON file")
        
        # Insert data
        insert_ngos(ngos_data)
        
        print("\nImport completed successfully!")
        
    except Exception as e:
        print(f"Error during import: {str(e)}")
        raise

if __name__ == '__main__':
    main()
