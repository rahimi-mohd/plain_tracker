# PLAIN TRACKER 

This project is an alternative for trackers apps, be it bugs, issues, or anything that user want to track. Main features include:
1. Authentication: Login, Signup, Logout.  
2. Create new issues.
3. See list of all issues.
4. See list of all own issues (create and assigned to).
5. See list of dropped issues.
6. Comment on issues.

## Hows To

To setup on local machine, follow this step:
1. Clone this repository `git clone <url>`.
2. Install dependencies `pip install -r requirements.txt`.
3. Create .env files to satisfied the environment in project's setting. eg:
```
DEBUG=False
SECRET_KEY=my-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
**NOTE**: You have to change your SECRET_KEY, add your ALLOWED_HOST and DATABASE_URL if you're deploying.   

4. Run `python manage.py collectstatic` to collect all static data like css/js/etc.
5. Run `python manage.py makemigrations` and then `python manage.py migrate` to record migrations and migrate database.
6. Run `python manage.py runserver` to activate/run server.  

**Optional**: 
Run `python manage.py createsuperuser` to add admin/super user account. This can help you to login easily without signup new user account, and this also can help you enter admin page `/admin/`.

## Technology Stack
1. Django
2. HTML
3. Bootstrap
4. HTMX