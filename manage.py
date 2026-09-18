#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

For more information on Django management commands, see:
https://docs.djangoproject.com/en/6.1/ref/django-admin/
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
      
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
