#!/bin/bash

# Build and start containers
docker compose -f docker-compose.dev.yml up --build -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Run migrations
docker compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser if it doesn't exist
docker compose -f docker-compose.dev.yml exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
"

echo "Development environment is ready!"
echo "Django server: http://localhost:8000"
echo "Admin interface: http://localhost:8000/admin"
echo "Username: admin"
echo "Password: admin" 