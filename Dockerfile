# Dockerfile for Django Applications

# Section 1- Base Image
FROM python:3.11.2-slim
RUN apt update && apt upgrade -y
RUN apt install libpq-dev python3-dev gcc -y
RUN mkdir app/
COPY . /app/
WORKDIR /app/
ARG DB_HOST
ENV DB_HOST=$DB_HOST
ARG DB_PASSWORD
ENV DB_PASSWORD=$DB_PASSWORD
ARG STRIPE_PRIVATE_KEY
ENV STRIPE_PRIVATE_KEY=$STRIPE_PRIVATE_KEY
ARG STRIPE_WEBHOOK
ENV STRIPE_WEBHOOK=$STRIPE_WEBHOOK
ARG EMAIL_HOST
ENV EMAIL_HOST=$EMAIL_HOST
ARG EMAIL_HOST_USER
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD





RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000