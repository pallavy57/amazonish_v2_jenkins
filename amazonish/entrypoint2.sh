#!/usr/bin/env bash
# entrypoint2.sh

python3 manage.py crontab add
python3 manage.py crontab show


# Then run the main container command (passed to us as arguments)
exec "$@"



