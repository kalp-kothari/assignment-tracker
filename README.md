# Django Assignment Tracker

A simple Django app to track assignments per logged-in user.

## Features
- Login / authentication (signup, login, logout)
- Add / view / edit / delete assignments
- Track due dates
- Mark assignments completed / pending
- Assignments are always scoped to the logged-in user

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Then visit http://127.0.0.1:8000/ — you'll be redirected to login.
Click "Sign up" to create an account, then log in.

## Project layout
- `tracker_project/` — Django project settings/urls
- `assignments/` — the app: models, views, forms, urls, templates
  - `templates/assignments/` — assignment list/add/edit/delete pages
  - `templates/registration/` — login/signup pages

---

## Pushing to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Django Assignment Tracker"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

`db.sqlite3`, `venv/`, and `staticfiles/` are already excluded via `.gitignore` — you
never want your local database or virtual environment committed.

---

## Deploying (Render — free, simplest option)

This project is already set up for a standard cloud deploy:
- `gunicorn` — production web server (Django's `runserver` is dev-only)
- `whitenoise` — serves CSS/static files without needing a separate service
- `dj-database-url` — lets the app switch from SQLite to Postgres via one env var
- `Procfile` — tells the host how to start the app
- Settings now read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from environment
  variables instead of being hardcoded

### Steps (Render.com)
1. Push your code to GitHub (above) if you haven't already.
2. Go to https://render.com → sign up/log in with GitHub.
3. **New +** → **Web Service** → connect your GitHub repo.
4. Render auto-detects Python. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn tracker_project.wsgi`
5. Add environment variables (Render dashboard → Environment):
   - `SECRET_KEY` — generate one with:
     `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `<your-app-name>.onrender.com`
6. **(Optional but recommended)** Add a free Postgres database from Render's
   dashboard (New + → PostgreSQL) — Render gives you a connection string,
   copy it into an env var named `DATABASE_URL` on your web service.
   Without this, SQLite is used, but most hosts wipe the filesystem on
   redeploy, so your data won't persist — fine for a demo, not for real use.
7. Deploy. Once live, visit `<your-app-name>.onrender.com/admin/` and run
   `createsuperuser` via Render's Shell tab if you need an admin login there.

### Alternative hosts
The same `Procfile` / `requirements.txt` setup also works on **Railway** and
**Heroku**, with the same environment variables. PythonAnywhere is another
free option but uses a different (manual WSGI) setup rather than a Procfile.

## Notes
- Locally, `DEBUG` defaults to `True` and SQLite is used automatically — no
  env vars needed for local dev.
- Never commit a real `.env` file or your production `SECRET_KEY` to GitHub.
  `.env.example` shows the shape without real secrets.
