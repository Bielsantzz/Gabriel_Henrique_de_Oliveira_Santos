import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Responsaveis

class Command(BaseCommand):
    help = "Importa responsaveis de population/responsaveis.csv usando pandas (com limpeza e validação)."

    def add_arguments(self, parser):
        parser.add_argument("--arquivo_responsaveis", default=str(Path("population") / "responsaveis.csv"))
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os responsaveis antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create) em vez de inserir em massa")

    @transaction.atomic 
    def handle(self, *args, **opts):
        csv_path = Path(opts["arquivo_responsaveis"]) 
        if not csv_path.exists(): 
            raise CommandError(f"Arquivo não encontrado: {csv_path}")

        df = pd.read_csv(csv_path)

        for col in ["nome"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            else:
                df[col] = ""

        df = df.dropna(how="all")
        df = df.drop_duplicates(subset=["nome"], keep="first").reset_index(drop=True)

        obrigatorios = df["nome"].ne("") 
        invalidos = df[~obrigatorios]
        if not invalidos.empty: 
            self.stdout.write(self.style.WARNING(f"Pulando {len(invalidos)} linha(s) inválida(s)."))

        df = df[obrigatorios]

        if opts["truncate"]:
            self.stdout.write(self.style.WARNING("Limpando tabela api_responsaveis..."))
            Responsaveis.objects.all().delete()

        criados = 0
        atualizados = 0

        if opts["update"]: 
            for row in df.itertuples(index=False):
                obj, created = Responsaveis.objects.update_or_create(
                    nome=row.nome
                )

                if created:
                    criados += 1
                else:
                    atualizados += 1
        else:
            buffer = []
            for row in df.itertuples(index=False):
                buffer.append(Responsaveis(
                    nome=row.nome
                ))
            Responsaveis.objects.bulk_create(buffer, ignore_conflicts=True)
            criados = len(buffer)

        msg = f"Concluído. Criado: {criados}"
        if opts["update"]:
            msg += f" | Atualizados: {atualizados}"
        self.stdout.write(self.style.SUCCESS(msg))