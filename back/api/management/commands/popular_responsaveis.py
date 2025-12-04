import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Responsaveis

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="population/Responsaveis.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):

        df = pd.read_csv(o["arquivo"], encoding="utf-8")

        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        if o["truncate"]:
            Responsaveis.objects.all().delete()

        df['nome'] = df['nome'].astype(str).str.strip()

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                obj, created = Responsaveis.objects.update_or_create(
                    responsavel=r.nome,
                    defaults={"responsavel": r.nome}
                )

                if created:
                    criados += 1
                else:
                    atualizados += 1

            self.stdout.write(self.style.SUCCESS(f'criados: {criados} | atualizados: {atualizados}'))

        else:
            objs = [
                Responsaveis(responsavel=r.nome)
                for r in df.itertuples(index=False)
            ]

            Responsaveis.objects.bulk_create(objs, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))

