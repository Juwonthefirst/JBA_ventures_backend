from django.apps import AppConfig


class PropertyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'v1.property'
    
    def ready(self):
        from v1.property import signals
