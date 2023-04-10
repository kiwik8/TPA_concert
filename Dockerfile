# Dockerfile for Django Applications

# Section 1- Base Image
FROM python:3.11.2-slim
RUN apt update && apt upgrade -y
RUN apt install libpq-dev -y
RUN mkdir app/
COPY . /app/
WORKDIR /app/
RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
