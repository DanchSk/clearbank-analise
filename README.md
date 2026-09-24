# ClearBank — Análise Financeira

Notebook Python que lê e valida `transacoes.csv`, calcula métricas mensais, sinaliza movimentações suspeitas e exporta `relatorio.json`.

## Como executar

1. Abra `desafio-final.ipynb` no [Google Colab](https://colab.research.google.com/github/DanchSk/clearbank-analise/blob/main/desafio-final.ipynb) ou no Jupyter (Python 3.10+).
2. Execute todas as células em ordem (no Colab: Ambiente de execução → Executar tudo).
3. No Colab o notebook abre sozinho, sem os outros arquivos do repositório. A primeira célula cria `transacoes.csv` se ele ainda não estiver na sessão. Se o arquivo já existir na pasta, ele é reutilizado.

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
