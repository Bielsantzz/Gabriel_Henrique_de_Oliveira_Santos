from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Popula o histórico'

    def handle(self, *args, **options):
        # código do comando
        self.stdout.write('Comando executado com sucesso!')
