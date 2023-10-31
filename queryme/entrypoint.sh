#!/bin/sh

TRIES=0
MAX_TRIES=30
DB_READY=0

echo "Waiting for PostgreSQL to become ready..."

while [ $TRIES -lt $MAX_TRIES ]; do
  pg_isready -h db -U user -d mysuperdata
  if [ $? = 0 ]; then
    echo "Checking if Django can connect to database..."
    python manage.py check --database default
    if [ $? = 0 ]; then
      DB_READY=1
      break
    fi
  fi
  echo "Not ready yet..."
  sleep 1
  TRIES=$((TRIES + 1))
done

if [ $DB_READY = 0 ]; then
  echo "Error: PostgreSQL did not become ready in time."
  exit 1
fi

echo "PostgreSQL is ready."
python manage.py migrate

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'Data29102023') if not User.objects.filter(username='admin').exists() else None"

exec "$@"
