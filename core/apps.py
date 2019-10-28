from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Главное'

    def ready(self):
        try:
            import core.signals
        except ImportError:
            raise ImportError('Error in Importing signals.py')

        try:
            from scheduler import backupScheduler
            backupScheduler.start()
        except ImportError:
            raise ImportError('Error in importing backupScheduler.py')

