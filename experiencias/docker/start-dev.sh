#!/bin/bash
# docker compose down -v
# Build and start containers
docker compose -f docker-compose.dev.yml up --build -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Apply migrations
docker compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser if it doesn't exist
docker compose -f docker-compose.dev.yml exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

# Collect static files
docker compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

echo "Development environment is ready!"
echo "Django server: http://localhost:8000"
echo "Admin interface: http://localhost:8000/admin"
echo "Username: admin"
echo "Password: admin" 

# Show logs
docker compose -f docker-compose.dev.yml logs -f

