#### FILE START
#!/bin/bash

if [ -z "$PORT" ]
then
    #echo "\$PORT is empty"
    PORT=8000
fi

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput


python manage.py makemigrations
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


python manage.py clearsessions
# Start server
echo "Starting server on PORT:$PORT"
python manage.py runserver 0.0.0.0:$PORT
