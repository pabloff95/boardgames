## Backend

Run backend with docker:

1. `docker compose build`
2. `docker compose up`

Run backend without docker:

1. Navigate to the backend folder: `cd backend`
2. Activate venv: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python manage.py runserver`

Format code: `black .`
Update `requirements.txt`: `rm requirements.txt && pip freeze > requirements.txt`
Run tests: `python manage.py test`

## Frontend
