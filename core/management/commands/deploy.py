import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда для деплоя. По умолчанию деплоим на тестовый, ' \
           'при деплое на production нужно передать аргумент --prod'

    command = 'ansible-playbook -i config/deploy/hosts/{} config/deploy/deploy.yml'

    def add_arguments(self, parser):
        parser.add_argument(
            '--prod',
            action='store_const',
            const='prod',
            default='test',
            help="Делой на прод"
        )

    def handle(self, *args, **options):
        command = self.command.format(options.get('prod'))
        subprocess.call(command, shell=True)
