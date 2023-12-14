from django.apps import AppConfig
from django.core.signals import request_finished

class VmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vms'

    def ready(self):
        import django.core.signals