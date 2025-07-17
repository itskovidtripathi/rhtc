import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rare_and_hard_to_treat_cancers.settings')
django.setup()

from apps.cancer_centers.models import CancerHospitals

def import_hospitals():
    # Read CSV file
    df = pd.read_csv('hospital_data.csv')
    
    # Counter for successful imports
    success_count = 0
    
    print("Starting import process...")
    
    for _, row in df.iterrows():
        try:
            # Create hospital object
            hospital = CancerHospitals(
                host_code=row['host_code'],
                hospital=row['hospital'],
                center=row['center'],
                pin_code=row['pin_code'],
                geo_location=row['geo_location'],
                city=row['city'],
                region=row['region'],
                country=row['country'],
                phone_tel=row['phone_tel'] if row['phone_tel'] != 0 else None,
                website=row['website'] if row['website'] != 'none' else '',
                review=row['review'],
                review_count=row['review_count'],
                wheelchair=row['wheelchair'],
                blood_bank=row['blood_bank'],
                pathology=row['pathology'],
                tags=row['tags'],
                coords=row['coords'],
                hospital_policy=row['hospital_policy'] if row['hospital_policy'] != 'none' else None,
                palliative_care=row['palliative_care'],
                diagnosis_center=row['diagnosis_center']
            )
            hospital.save()
            success_count += 1
            print(f"Successfully imported: {row['hospital']}")
            
        except Exception as e:
            print(f"Error importing {row['hospital']}: {str(e)}")
    
    print(f"\nImport completed. Successfully imported {success_count} hospitals.")

if __name__ == "__main__":
    import_hospitals()
