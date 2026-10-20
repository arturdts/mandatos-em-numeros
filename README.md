# Mandatos em Números

Estudo de dados sobre o câmbio, a bolsa, os juros, a inflação, o salário mínimo e o PIB em cada mandato presidencial desde o Plano Real (1994).

Cada período começa meses antes da eleição e traz os acontecimentos nacionais e internacionais da época. Todos os mandatos são medidos com as mesmas regras.

## O que tem no site

- Filtro por presidente, de FHC 1 a Lula 3, com zoom por ano
- Câmbio, Ibovespa, Selic, IPCA, salário mínimo, PIB e commodities
- Comparação com moedas e bolsas de outros países emergentes
- As cinco maiores empresas da bolsa no início de cada mandato
- Marcos históricos, separados em eventos globais e nacionais
- Tabela comparativa com valores anualizados

## Fontes

- **Banco Central do Brasil** (SGS): dólar (3698), Selic (4189), IPCA 12 meses (13522), IPCA mensal (433), salário mínimo (1619), PIB (7326) e índice de commodities IC-Br (27574)
- **Yahoo Finance**: Ibovespa, dólar, moedas de emergentes, ETFs EWZ e EEM e ações da B3

## Arquivos

| Arquivo | Função |
|---|---|
| `index.html` | O site |
| `dados.js` | Os números, gerados pelo script |
| `fetch_data.py` | Baixa as séries e atualiza o `dados.js` |

## Como atualizar os dados

```
pip install yfinance pandas requests
python fetch_data.py
```

Depois, é só enviar o novo `dados.js` para o repositório.
