"""
fipe_marca_sync.py
==================
Compara marcas de veículos de um arquivo SQL da FIPE com uma base CSV existente
e gera um CSV com apenas as marcas novas, com IDs sequenciais.

Uso:
    python fipe_marca_sync.py
    python fipe_marca_sync.py --base veiculo_marca.csv --sql fipe.sql --saida novas_marcas.csv
"""

import argparse
import os
import re
import sys

import pandas as pd


TYPE_MAP: dict[str, int] = {
    "carros": 0,
    "motos": 1,
    "caminhoes": 2,
    "micro-onibus": 2,
}

_SQL_PATTERN = re.compile(
    r"VALUES\s*\(\s*\d+\s*,\s*N'([^']+)'\s*,\s*\d+\s*,\s*N'([^']+)'",
    re.IGNORECASE,
)




def extrair_marcas_sql(caminho_sql: str) -> dict[str, dict]:
    """
    Lê o arquivo SQL e retorna um dicionário indexado pelo nome em minúsculas.

    Retorno:
        {
            "honda": {"original": "Honda", "tipo": "motos"},
            ...
        }
    """
    marcas: dict[str, dict] = {}

    print(f"[1/3] Lendo SQL: {caminho_sql}")
    with open(caminho_sql, encoding="utf-8", errors="replace") as f:
        for linha in f:
            m = _SQL_PATTERN.search(linha)
            if m:
                tipo, nome = m.group(1), m.group(2)
                chave = nome.lower().strip()
                marcas.setdefault(chave, {"original": nome, "tipo": tipo})

    print(f"      {len(marcas)} marcas extraídas do SQL.")
    return marcas


def carregar_base_existente(caminho_csv: str) -> tuple[set[str], int]:
    """
    Lê o CSV base e devolve (conjunto de nomes em minúsculas, maior ID atual).
    """
    print(f"[2/3] Lendo base existente: {caminho_csv}")
    df = pd.read_csv(caminho_csv, sep=None, engine="python", encoding="latin1")

    nomes = set(df["name"].astype(str).str.lower().str.strip())
    maior_id = int(df["id_veiculo_marca"].max())

    print(f"      {len(nomes)} marcas já cadastradas. Maior ID: {maior_id}.")
    return nomes, maior_id


def gerar_novas_marcas(
    marcas_sql: dict[str, dict],
    nomes_existentes: set[str],
    maior_id: int,
) -> pd.DataFrame:
    """
    Filtra marcas ainda não cadastradas e atribui IDs sequenciais.
    """
    novas = [
        {
            "name": dados["original"],
            "status": 1,
            "type": TYPE_MAP.get(dados["tipo"], 0),
        }
        for chave, dados in marcas_sql.items()
        if chave not in nomes_existentes
    ]

    if not novas:
        return pd.DataFrame()

    df = pd.DataFrame(novas)
    df.insert(0, "id_veiculo_marca", range(maior_id + 1, maior_id + 1 + len(df)))
    return df



def processar(base_csv: str, novo_sql: str, saida_csv: str) -> None:
    for path in (base_csv, novo_sql):
        if not os.path.exists(path):
            sys.exit(f"ERRO: arquivo não encontrado → {path}")

    nomes_existentes, maior_id = carregar_base_existente(base_csv)
    marcas_sql = extrair_marcas_sql(novo_sql)

    print("[3/3] Identificando novas marcas…")
    df_novas = gerar_novas_marcas(marcas_sql, nomes_existentes, maior_id)

    if df_novas.empty:
        print("Nenhuma marca nova encontrada. Nada foi salvo.")
        return

    df_novas.to_csv(saida_csv, index=False, sep=";", encoding="utf-8-sig")
    print(f"\n✔  {len(df_novas)} novas marcas salvas em: {saida_csv}")



def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza marcas FIPE com a base de veículos."
    )
    parser.add_argument(
        "--base",
        default="veiculo_marca.csv",
        help="CSV com marcas já cadastradas (padrão: veiculo_marca.csv)",
    )
    parser.add_argument(
        "--sql",
        default="fipe-02122025-MSSQL.sql",
        help="Arquivo SQL da FIPE com os novos dados",
    )
    parser.add_argument(
        "--saida",
        default="novas_marcas.csv",
        help="Nome do CSV de saída (padrão: novas_marcas.csv)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    processar(args.base, args.sql, args.saida)
