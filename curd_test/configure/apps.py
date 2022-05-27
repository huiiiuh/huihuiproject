from django.apps import AppConfig


class ConfigureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configure'

    def ready(self):
        import apps.configure.signals