# from django.apps import AppConfig


# class CordappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'CordApp'


from django.apps import AppConfig

class CordappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CordApp'

    def ready(self):
        # This imports the signals file you are about to create
        import CordApp.signals