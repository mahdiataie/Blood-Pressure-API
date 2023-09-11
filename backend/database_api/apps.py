from django.apps import AppConfig


# class DatabaseApiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'database_api'

class DatabaseApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database_api'
    
    def ready(self):
        import database_api.signals