from setuptools import setup

setup(
    name='django-command-cron',
    version='2021.7.10',
    packages=[
        'django_command_cron',
        'django_command_cron.admin',
        'django_command_cron.management',
        'django_command_cron.management.commands',
        'django_command_cron.migrations',
        'django_command_cron.models'
    ]
)
