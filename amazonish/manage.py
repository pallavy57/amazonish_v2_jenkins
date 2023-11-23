#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from venv import logger
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ImproperlyConfigured
def check_ping():
    hostname = "www.google.com"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    
    return pingstatus

# https://www.youtube.com/watch?v=Oy4v8HAbWCs
def healthcheck_view():

    try:
        isConnected = check_ping()
        print(isConnected)

        if (isConnected == "Network Active"):
            main()
        else:
            print("There is no internet connectivity")    

    except ImproperlyConfigured as ex:
        # Database is not configured (DATABASE_URL may not be set)
        print(ex)
        logger.error(
            "No Database connection Found!"
        )
    except OperationalError as op:
        # Database is not accessible
        print(op)
        logger.error(
            "No Database connection Found!"
        )


# https://codeburst.io/getting-started-with-kubernetes-deploy-a-docker-container-with-kubernetes-in-5-minutes-eb4be0e96370
# https://collabnix.com/kubernetes-on-docker-desktop-in-2-minutes/


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazonish.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # healthcheck_view()
    main()
