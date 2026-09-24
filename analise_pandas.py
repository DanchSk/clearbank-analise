"""RO1 — versão alternativa com pandas; compara com relatorio.json do notebook."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

LIMITE_SUSPEITO = 10000.00
CSV_PATH = Path(__file__).with_name("transacoes.csv")
JSON_PATH = Path(__file__).with_name("relatorio.json")


def carregar_validas(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, dtype=str)
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["cliente_id"] = df["cliente_id"].fillna("").str.strip()
    df["tipo"] = df["tipo"].fillna("").str.strip().str.lower()

    mask = (
        df["id"].notna()
        & df["cliente_id"].ne("")
        & df["data"].notna()
        & df["tipo"].isin(["credito", "debito"])
        & df["valor"].notna()
        & (df["valor"] > 0)
    )
    limpo = df.loc[mask].copy()
    limpo["id"] = limpo["id"].astype(int)
    limpo["mes"] = limpo["data"].dt.strftime("%Y-%m")
    return limpo


def resumo_mensal(df: pd.DataFrame) -> dict:
    agrupado = df.groupby("mes", sort=True)
    saida = {}
    for mes, grupo in agrupado:
        credito = float(grupo.loc[grupo["tipo"] == "credito", "valor"].sum())
        debito = float(grupo.loc[grupo["tipo"] == "debito", "valor"].sum())
        valores = grupo["valor"]
        saida[mes] = {
            "quantidade": int(len(grupo)),
            "total_credito": round(credito, 2),
            "total_debito": round(debito, 2),
            "saldo": round(credito - debito, 2),
            "media": round(float(valores.mean()), 2),
            "maior_valor": float(valores.max()),
            "menor_valor": float(valores.min()),
        }
    return saida


def quase_igual(a: float, b: float, tol: float = 0.01) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> int:
    if not CSV_PATH.exists():
        print(f"Arquivo não encontrado: {CSV_PATH}")
        return 1
    if not JSON_PATH.exists():
        print(
            f"{JSON_PATH.name} não encontrado. "
            "Execute o notebook (ou clearbank.py) antes de comparar."
        )
        return 1

    df = carregar_validas(CSV_PATH)
    pandas_resumo = resumo_mensal(df)
    with JSON_PATH.open(encoding="utf-8") as f:
        nativo = json.load(f)

    print("===== RESUMO PANDAS =====")
    for mes, m in pandas_resumo.items():
        print(
            f"{mes}: q={m['quantidade']} credito={m['total_credito']} "
            f"debito={m['total_debito']} saldo={m['saldo']}"
        )

    divergencias = []
    nativo_resumo = nativo.get("resumo_mensal", {})
    if set(pandas_resumo) != set(nativo_resumo):
        divergencias.append(
            f"meses distintos: pandas={sorted(pandas_resumo)} "
            f"nativo={sorted(nativo_resumo)}"
        )

    for mes, m in pandas_resumo.items():
        ref = nativo_resumo.get(mes)
        if ref is None:
            continue
        for chave in (
            "quantidade",
            "total_credito",
            "total_debito",
            "saldo",
            "media",
            "maior_valor",
            "menor_valor",
        ):
            if chave == "quantidade":
                if int(m[chave]) != int(ref[chave]):
                    divergencias.append(f"{mes}.{chave}: {m[chave]} != {ref[chave]}")
            elif not quase_igual(m[chave], ref[chave]):
                divergencias.append(f"{mes}.{chave}: {m[chave]} != {ref[chave]}")

    if divergencias:
        print("\nDIVERSÊNCIAS:")
        for d in divergencias:
            print(f" - {d}")
        return 1

    print("\nOK: resultados iguais (pandas == relatorio.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
