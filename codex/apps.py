from django.apps import AppConfig


class CodexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codex'

    def ready(self):
        """ Once the app is up and running ensure the signals are connected """
        import codex.signals