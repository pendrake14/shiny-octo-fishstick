#!/bin/bash
set -e

docker compose -f docker-compose.dev.yml run --rm web sh -c "
    coverage run manage.py test users --verbosity=2 &&
    coverage report
"