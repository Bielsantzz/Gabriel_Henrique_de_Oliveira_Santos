import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Ambientes

class Command(BaseCommand):
    help = "Importa ambientes de population/ambientes.csv usando pandas (com limpeza e validação)."

    def add_arguments(self, parser):
        parser.add_argument("--arquivo_ambientes", default=str(Path("population") / "ambientes.csv"))
        parser.add_argument("--arquivo_locais", default=str(Path("population") / "locais.csv"))
        parser.add_argument("--arquivo_responsaveis", default=str(Path("population") / "responsaveis.csv"))
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os ambientes antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create) em vez de inserir em massa")

    @transaction.atomic
    def handle(self, *a, **o):
        df_ambientes = pd.read_csv(o["arquivo_ambientes"], encoding="utf-8-sig")
        df_locais = pd.read_csv(o["arquivo_locais"], encoding="utf-8-sig")
        df_responsaveis = pd.read_csv(o["arquivo_responsaveis"], encoding="utf-8-sig")
        df_ambientes.columns = [c.strip().lower().lstrip("\ufeff") for c in df_ambientes.columns]
        df_locais.columns = [c.strip().lower().lstrip("\ufeff") for c in df_locais.columns]
        df_responsaveis.columns = [c.strip().lower().lstrip("\ufeff") for c in df_responsaveis.columns]

        df_responsaveis['id'] = df_responsaveis.index + 1

        df_locais['local'] = df_locais.index + 1

        df_ambientes['local'] = df_locais['local']

        df_responsaveis['nome'] = df_responsaveis.index + 1

        mapa_responsaveis = dict(zip(df_responsaveis['nome'], df_ambientes['responsavel']))

        df_ambientes['responsavel'] = df_responsaveis["nome"].map(mapa_responsaveis)
        
        if o["truncate"]: Ambientes.objects.all().delete()
 
        df_ambientes['local']=df_ambientes["local"].astype(int)
        df_ambientes['descricao']=df_ambientes["descricao"].astype(str).str.strip()
        df_ambientes['responsavel']=df_ambientes["responsavel"].astype(int)
    
        if o["update"]:
            criados = atualizados = 0
            for r in df_ambientes.itertuples(index=False):
                _, created = Ambientes.objects.update_or_create(
                    isbn=r.isbn,
                    defaults={
                        "local": int(r.local),
                        "descricao": r.descricao or "",
                        "responsavel": int(r.responsavel)
                    },
                )

            criados += int(created)          
            atualizados += int(not created)   
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
 
        else:
            objs = []
            for r in df_ambientes.itertuples(index=False):
                objs.append(
                    Ambientes(
                        local_id=int(r.local),
                        descricao=r.descricao or "",
                        responsavel_id=int(r.responsavel)
                    )
                )
            Ambientes.objects.bulk_create(objs, ignore_conflicts=True)
            criados = len(objs)
 
 
            self.stdout.write(self.style.SUCCESS(f"Criados: {len(objs)}"))