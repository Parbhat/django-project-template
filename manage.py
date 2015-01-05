#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # import the settings here to preload the ENV settings
    import {{ project_name }}.settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings.development")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
