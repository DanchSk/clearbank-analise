# ClearBank — Análise Financeira

Notebook Python que lê e valida `transacoes.csv`, calcula métricas mensais, sinaliza movimentações suspeitas e exporta `relatorio.json`.

## Como executar

1. Abra `desafio-final.ipynb` no Google Colab ou Jupyter (Python 3.10+).
2. Garanta que `transacoes.csv` está na mesma pasta do notebook.
3. Execute todas as células em ordem (Run All / Runtime → Run all).

Dependências opcionais (RO1/RO2):

```bash
pip install pandas matplotlib
python analise_pandas.py
```

## O que o notebook gera

- Relatório formatado no terminal (limpeza, métricas mensais, suspeitas)
- `relatorio.json` — totais, período, resumo mensal e lista de suspeitas
- `grafico.png` — barras do saldo mensal (crédito − débito)

## Estrutura

```
clearbank-analise/
├── desafio-final.ipynb   # solução principal (saídas salvas)
├── transacoes.csv        # dados de entrada
├── analise_pandas.py     # RO1 — alternativa com pandas
├── grafico.png           # RO2 — saldo mensal
└── README.md
```

`relatorio.json` é gerado na execução e não precisa estar versionado.
