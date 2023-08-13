from django.apps import AppConfig


class CarsManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars_management'
    label = 'cars_management'

    def ready(self):
        from .views import create_groups
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_groups, sender=self)