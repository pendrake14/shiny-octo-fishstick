# Variables
COMPOSE = docker compose -f docker-compose.dev.yml
SERVICE = web

# Inicializar entorno de desarrollo
start:
	$(COMPOSE) up --build -d
	@echo "Waiting for database to be ready..."
	sleep 10
	$(COMPOSE) exec $(SERVICE) python manage.py migrate
	$(COMPOSE) exec $(SERVICE) python manage.py collectstatic --noinput
	$(COMPOSE) logs -f


# Tests con coverage
test:
	$(COMPOSE) run --rm $(SERVICE) sh -c "coverage run manage.py test users --verbosity=2 && coverage report"

# Crear nuevas migraciones
migrations:
	$(COMPOSE) run --rm $(SERVICE) python manage.py makemigrations

# Aplicar migraciones
migrate:
	$(COMPOSE) run --rm $(SERVICE) python manage.py migrate

# Recolectar archivos estáticos
collectstatic:
	$(COMPOSE) run --rm $(SERVICE) python manage.py collectstatic --noinput

# Crear superusuario (hardcoded)
createsuperuser:
	$(COMPOSE) exec $(SERVICE) python manage.py shell -c \
	"from django.contrib.auth import get_user_model; \
	User = get_user_model(); \
	User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

# Apagar y limpiar
stop:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v
