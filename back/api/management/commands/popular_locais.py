
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Locais

class Command(BaseCommand):
    help = "Importa locais de population/locais.csv usando pandas (com limpeza e validação)."

    def add_arguments(self, parser):
        parser.add_argument("--arquivo_locais", default=str(Path("population") / "locais.csv"))
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os locais antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create) em vez de inserir em massa")

    @transaction.atomic 
    def handle(self, *args, **opts):
        csv_path = Path(opts["arquivo_locais"]) 
        if not csv_path.exists():
            raise CommandError(f"Arquivo não encontrado: {csv_path}")

        df = pd.read_csv(csv_path)

        for col in ["local"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            else:
                df[col] = ""

        df = df.dropna(how="all")
        df = df.drop_duplicates(subset=["local"], keep="first").reset_index(drop=True)

        obrigatorios = df["local"].ne("") 
        invalidos = df[~obrigatorios] 
        if not invalidos.empty: 
            self.stdout.write(self.style.WARNING(f"Pulando {len(invalidos)} linha(s) inválida(s)."))

        df = df[obrigatorios]

        if opts["truncate"]:
            self.stdout.write(self.style.WARNING("Limpando tabela api_locais..."))
            Locais.objects.all().delete()

        criados = 0
        atualizados = 0

        if opts["update"]: 
            for row in df.itertuples(index=False):
                obj, created = Locais.objects.update_or_create(
                    local=row.local
                )

                if created:
                    criados += 1
                else:
                    atualizados += 1
        else:
            buffer = []
            for row in df.itertuples(index=False):
                buffer.append(Locais(
                    local=row.local
                ))
            Locais.objects.bulk_create(buffer, ignore_conflicts=True)
            criados = len(buffer)

        msg = f"Concluído. Criado: {criados}"
        if opts["update"]:
            msg += f" | Atualizados: {atualizados}"
        self.stdout.write(self.style.SUCCESS(msg))
