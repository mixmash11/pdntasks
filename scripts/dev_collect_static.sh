#!/bin/bash
#### Description: collects static assets
docker-compose -f local.yml run --rm django python manage.py collectstatic --noinput
