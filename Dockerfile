# ---- Base ----
FROM ubuntu:latest AS base
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# ---- App ----
FROM base AS app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# ---- Release ----
FROM app AS release
RUN ["python manage.py db upgrade"]

# ---- Web ---
FROM release AS web
CMD ["python manage.py runserver --host 0.0.0.0 --port ${PORT}"]
