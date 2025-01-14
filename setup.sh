#!/bin/bash

echo "Starting database migrations..."

# Make migrations
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Error: Failed to make migrations"
    exit 1
fi

# Apply migrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to apply migrations"
    exit 1
fi

# Run development server
echo "Starting development server..."
python manage.py runserver