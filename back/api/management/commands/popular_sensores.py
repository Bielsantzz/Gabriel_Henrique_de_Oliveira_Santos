
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Sensores, Ambientes, Historico
from django.utils import timezone

class Command(BaseCommand):
    help = "Importa sensores do CSV population/sensores.csv"

    def add_arguments(self, parser):
        parser.add_argument("--arquivo_sensores", default="population/sensores.csv")
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os sensores antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create)")

    @transaction.atomic
    def handle(self, *args, **options):

        df = pd.read_csv(options["arquivo_sensores"], encoding="utf-8-sig")
        df.columns = [c.strip().lower() for c in df.columns]

        # Limpeza e tipagem
        df["sensor"] = df["sensor"].astype(str).str.strip()
        df["mac_address"] = df["mac_address"].astype(str).str.strip()
        df["unidade_medida"] = df["unidade_medida"].astype(str).str.strip()
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
        df["status"] = df["status"].astype(bool)

        df["ambiente_id"] = df["ambiente"].astype(int)

        # Validar se os ambientes existem
        ids_ambientes = set(Ambientes.objects.values_list("id", flat=True))
        ids_utilizados = set(df["ambiente_id"].unique())
        ids_faltando = ids_utilizados - ids_ambientes
        if ids_faltando:
            raise CommandError(f"Os seguintes ambientes NÃO existem no banco: {ids_faltando}")

        if options["truncate"]:
            Sensores.objects.all().delete()

        if options["update"]:
            criados = 0
            atualizados = 0
            for r in df.itertuples(index=False):
                obj, created = Sensores.objects.update_or_create(
                    sensor=r.sensor,
                    mac_address=r.mac_address,
                    defaults={
                        "unidade_medida": r.unidade_medida,
                        "latitude": r.latitude,
                        "longitude": r.longitude,
                        "status": r.status,
                        "ambiente_id": r.ambiente_id,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))

            if created:
                Historico.objects.update_or_create(
                    sensor = obj,
                    valor = 10.5,
                    timestamp = timezone.now()
                    )
        
        else:
            objs = []
            for r in df.itertuples(index=False):
                obj = Sensores.objects.create(
                        sensor=r.sensor,
                        mac_address=r.mac_address,
                        unidade_medida=r.unidade_medida,
                        latitude=r.latitude,
                        longitude=r.longitude,
                        status=r.status,
                        ambiente_id=r.ambiente_id,
                )
                
                
                
                Historico.objects.update_or_create(
                    sensor = obj,
                    valor = 10.5,
                    timestamp = timezone.now()
                )
            Sensores.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Sensores criados: {len(objs)}"))
