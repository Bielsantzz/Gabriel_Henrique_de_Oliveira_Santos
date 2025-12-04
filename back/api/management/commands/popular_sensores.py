from django.core.management.base import BaseCommand
from api.models import Sensores
import pandas as pd
from datetime import datetime

def parse_status(val):
    if isinstance(val, str):
        val_lower = val.lower()
        if val_lower in ["ativo", "true", "1"]:
            return True
        elif val_lower in ["inativo", "false", "0"]:
            return False
    elif isinstance(val, (int, float)):
        return bool(val)
    return False

class Command(BaseCommand):
    help = "Popula a tabela Sensores"

    def add_arguments(self, parser):
        parser.add_argument('--truncate', action='store_true', help='Apaga todos os sensores antes')
        parser.add_argument('--update', action='store_true', help='Atualiza os sensores existentes')

    def handle(self, *args, **options):
        df = pd.read_csv("population/sensores.csv")
        
        df['status'] = df['status'].apply(parse_status)

        if options["truncate"]:
            Sensores.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Todos os sensores foram apagados"))

        objs_criar = []
        objs_atualizar = []

        for r in df.itertuples(index=False):
            try:
                if options["update"]:
                    s = Sensores.objects.get(mac_address=r.mac_address)
                    s.sensor = r.sensor
                    s.unidade_med = r.unidade_medida
                    s.latitude = float(r.latitude) if pd.notna(r.latitude) else None
                    s.longitude = float(r.longitude) if pd.notna(r.longitude) else None
                    s.status = r.status
                    s.ambiente_id = int(r.ambiente)
                    objs_atualizar.append(s)
                    continue
            except Sensores.DoesNotExist:
                pass

            objs_criar.append(Sensores(
                sensor=r.sensor,
                mac_address=r.mac_address,
                unidade_med=r.unidade_medida,
                latitude=float(r.latitude) if pd.notna(r.latitude) else None,
                longitude=float(r.longitude) if pd.notna(r.longitude) else None,
                status=r.status,
                ambiente_id=int(r.ambiente),
                timestamp=datetime.now()
            ))

        if objs_criar:
            Sensores.objects.bulk_create(objs_criar)
        if objs_atualizar:
            Sensores.objects.bulk_update(objs_atualizar, ['sensor','unidade_med','latitude','longitude','status','ambiente_id'])

        self.stdout.write(self.style.SUCCESS(f"Registros criados: {len(objs_criar)}"))
        self.stdout.write(self.style.SUCCESS(f"Registros atualizados: {len(objs_atualizar)}"))
