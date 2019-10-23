from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'
    verbose_name = 'Финансовый учет'

    def ready(self):
        try:
            from schoolPaymentRecalculate import new_month_payment_calculate
            new_month_payment_calculate.start()
        except ImportError:
            raise ImportError('Error in importing new_month_payment_calculate')

