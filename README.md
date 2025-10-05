## Backend

To run the backend, first set up the `.env` file with your own data:

1. `cp backend/.env.example backend/.env`
2. Update the `backend/.env` settings

Run backend with docker (**recommended**):

1. `docker compose build`
2. `docker compose up`

Run backend without docker:

1. Navigate to the backend folder: `cd backend`
2. Activate venv: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python manage.py runserver`

### Backend commands

- Make migration: `docker compose exec django python backend/manage.py makemigrations`
- Migrate: `docker compose exec django python backend/manage.py migrate`
- Add super user `docker compose exec django python backend/manage.py createsuperuser`

### Other commands

Format code: `black .`

Update `requirements.txt`: `rm requirements.txt && pip freeze > requirements.txt`

Run tests: `python manage.py test`

## Frontend
