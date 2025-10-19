from django.apps import AppConfig

class SwiftLogixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SwiftLogix'

    def ready(self):
        # Import signals here if you add them later
        # from . import signals
        pass
