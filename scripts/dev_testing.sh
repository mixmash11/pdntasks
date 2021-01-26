# Run testing and coverage
docker-compose -f local.yml run django coverage run -m pytest
docker-compose -f local.yml run django coverage report
docker-compose -f local.yml run --rm django coverage html
chromium-browser htmlcov/index.html
