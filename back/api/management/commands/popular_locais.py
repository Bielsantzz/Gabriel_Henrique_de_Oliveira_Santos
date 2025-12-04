import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Sensores

class Command(BaseCommand):
    help = "Popula a tabela Sensores a partir de um CSV"


def add_arguments(self, parser):
    parser.add_argument("--arquivo", default="population/sensores.csv")
    parser.add_argument("--truncate", action="store_true")
    parser.add_argument("--update", action="store_true")

@transaction.atomic
def handle(self, *args, **options):
    df = pd.read_csv(options["arquivo"], encoding="utf-8")
    df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

    # Corrige status para True/False
    df['status'] = df['status'].apply(lambda x: str(x).lower() in ['ativo','true','1'])

    if options["truncate"]:
        Sensores.objects.all().delete()
        self.stdout.write(self.style.WARNING("Todos os sensores foram apagados"))

    if options["update"]:
        criados = atualizados = 0
        for r in df.itertuples(index=False):
            _, created = Sensores.objects.update_or_create(
                mac_address=r.mac_address,
                defaults={
                    "sensor": r.sensor,
                    "unidade_med": r.unidade_medida,
                    "latitude": float(r.latitude) if pd.notna(r.latitude) else None,
                    "longitude": float(r.longitude) if pd.notna(r.longitude) else None,
                    "status": r.status,
                    "ambiente_id": int(r.ambiente),
                }
            )
            criados += int(created)
            atualizados += int(not created)
        self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
        return

    objs = [
        Sensores(
            sensor=r.sensor,
            mac_address=r.mac_address,
            unidade_med=r.unidade_medida,
            latitude=float(r.latitude) if pd.notna(r.latitude) else None,
            longitude=float(r.longitude) if pd.notna(r.longitude) else None,
            status=r.status,
            ambiente_id=int(r.ambiente)
        )
        for r in df.itertuples(index=False)
    ]
    Sensores.objects.bulk_create(objs, ignore_conflicts=True)
    self.stdout.write(self.style.SUCCESS(f"Registros criados: {len(objs)}"))

