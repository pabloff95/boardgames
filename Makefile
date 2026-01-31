# Manage app containers
build:
	docker compose build
reset:
	docker compose down && docker compose up --build
run:
	docker compose up
stop:
	docker compose down

# Utils
ARGS ?= $(filter-out $@,$(MAKECMDGOALS))
test:
	docker compose exec django pytest ${ARGS}

format:
	docker compose exec django black . 

requirements:
	. backend/venv/bin/activate && rm backend/requirements.txt && pip freeze > backend/requirements.txt

# Django commands
make migrations:
	docker compose exec django python manage.py makemigrations

migrate:
	docker compose exec django python manage.py migrate

createsuperuser:
	docker compose exec django python manage.py createsuperuser

shell:
	docker compose exec django python manage.py shell