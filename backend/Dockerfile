FROM python:3.12-slim as dev

WORKDIR /backend

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev 

COPY backend/requirements.txt /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /backend/

EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]

