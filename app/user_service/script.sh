#!/bin/sh

echo "
Script for user
"

# Make migrations and apply them
rm user_conf_files/migrations/0001_initial.py

python3 manage.py makemigrations user_conf_files
python3 manage.py makemigrations && \
python3 manage.py migrate auth && \
python3 manage.py migrate --noinput 

if [ -n "$DJANGO_USER_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_USER_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_USER_SUPERUSER_EMAIL" ]; then
    python3 manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_USER_SUPERUSER_USERNAME" \
        --email "$DJANGO_USER_SUPERUSER_EMAIL" \
    || true
fi

# Start the Django development server
python3 manage.py runserver 0.0.0.0:8000
