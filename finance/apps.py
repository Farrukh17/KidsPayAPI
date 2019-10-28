from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'
    verbose_name = 'Финансовый учет'

    def ready(self):
        try:
            from scheduler import paymentScheduler
            paymentScheduler.start()
        except ImportError:
            raise ImportError('Error in importing paymentScheduler')

