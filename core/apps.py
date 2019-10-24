from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Главное'

    def ready(self):
        try:
            import core.signals
        except ImportError:
            raise ImportError('Error in Importing signals.py')

