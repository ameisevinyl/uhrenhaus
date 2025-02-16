#!/bin/bash

echo "🚀 Resetting SQLite database and Django migrations..."

# Delete old migrations
find meters/migrations/ -name "*.py" ! -name "__init__.py" -delete
find contacts/migrations/ -name "*.py" ! -name "__init__.py" -delete

# Remove SQLite database
rm -f db.sqlite3

echo "✅ Database and migrations deleted."

# Recreate migrations and apply them
python manage.py makemigrations contacts meters
python manage.py migrate

echo "✅ Migrations applied successfully."

# Create superuser interactively
echo "👤 Creating superuser: ameise..."
python manage.py createsuperuser --username ameise --email ameise@amei.se

echo "✅ Superuser 'ameise' created."

# Run the server (optional)
echo "🚀 Starting Django server..."
python manage.py runserver
