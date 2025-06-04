# Rare & Hard to Treat Cancers (RHTC) Project

A comprehensive platform for information and support related to rare and hard-to-treat cancers.

## Project Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/itskovidtripathi/rhtc.git
cd "Rare & Hard to Treat Cancers"
```

2. **Create and Activate Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Setup**
```bash
cd src
python manage.py migrate
```

5. **Load Initial Data**
```bash
# Load questions data
python data/insert_question_in_db.py
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Run Development Server**
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to access the application.

## Project Structure

