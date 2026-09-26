# Django Assignment Tracker

Simple Django app to track assignments per logged-in user.

## Features

- Login / signup / logout
- Add, view, edit, delete assignments
- Track due dates
- Mark completed / pending
- Each user only sees their own assignments

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Visit http://127.0.0.1:8000/
