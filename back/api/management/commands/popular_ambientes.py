import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Ambientes
 
class Command(BaseCommand):
 
    def add_arguments(self, parser, *args, **options):
        parser.add_argument("--arquivo", default="population/ambientes.csv") 
        parser.add_argument("--truncate", action="store_true")  
        parser.add_argument("--update", action="store_true")  
 
    @transaction.atomic
    def handle(self, *a, **o):
        df = pd.read_csv(o["arquivo"], encoding="utf-8")  
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]
        print(" ############# Ambientes ###########\n", df)        
        if o["truncate"]:
            Ambientes.objects.all().delete()
           
        df['locais']=df["locais"].astype(int)
        df['descricao']=df["descricao"].astype(str)
        df['responsavel']=df["responsavel"].astype(int)
 
        if o["update"]:
            criados = atualizados = 0  
            for r in df.itertuples(index=False):
                _, created = Ambientes.objects.update_or_create(
                    defaults={
                        'locais': r.locais,
                        'descricao': r.descricao,
                        'responsavel': r.responsavel
                        }
                )
                criados += int(created)
                atualizados += int(not created)
            
            
            self.stdout.write
            (self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))
 
        else:
            objs = []
            for r in df.itertuples(index=False):
                objs.append(
                    Ambientes(
                        locais_id=r.locais,
                        descricao=r.descricao,
                        responsavel_id=r.responsavel
                    )
                )
 
            Ambientes.objects.bulk_create(objs, ignore_conflicts=True)
            criados = len(objs)  
                 
            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))