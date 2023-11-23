#!/bin/sh
# entrypoint.sh
python3  manage.py makemigrations 
python3  manage.py migrate

# Then run the main container command (passed to us as arguments)
exec "$@"




