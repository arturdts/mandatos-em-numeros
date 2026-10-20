"""Mandatos em Números: atualiza o arquivo dados.js.

    pip install yfinance pandas requests
    python fetch_data.py
"""
import json
import time
from datetime import date

import pandas as pd
import requests
import yfinance as yf

INICIO = "1994-07"

BCB = {"usd": 3698, "selic": 4189, "ipca12": 13522, "ipcaMo": 433, "sm": 1619, "icbr": 27574}
MERCADO = {"ibov": "^BVSP", "brl": "BRL=X", "ewz": "EWZ", "eem": "EEM"}
MOEDAS = {"México": "MXN=X", "África do Sul": "ZAR=X", "Chile": "CLP=X",
          "Colômbia": "COP=X", "Índia": "INR=X", "Indonésia": "IDR=X"}
EMPRESAS = ["PETR4", "VALE3", "ITUB4", "BBDC4", "BBAS3", "ABEV3", "BPAC11"]


def bcb(codigo, inicio=1994):
    url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
           f"?formato=json&dataInicial=01/01/{inicio}&dataFinal=31/12/{date.today().year}")
    for tentativa in range(4):
        try:
            df = pd.DataFrame(requests.get(url, timeout=90).json())
            df.index = pd.to_datetime(df["data"], dayfirst=True).dt.strftime("%Y-%m")
            return pd.to_numeric(df["valor"], errors="coerce")
        except Exception:
            time.sleep(3 * (tentativa + 1))
    raise RuntimeError(f"Banco Central: série {codigo} não respondeu")


def yahoo(ticker):
    for tentativa in range(3):
        df = yf.download(ticker, start="1994-07-01", auto_adjust=True, progress=False)
        if not df.empty:
            close = df["Close"].squeeze().dropna()
            return close.groupby(close.index.strftime("%Y-%m")).last()
        time.sleep(3 * (tentativa + 1))
    print(f"aviso: {ticker} sem dados")
    return pd.Series(dtype=float)


def main():
    serie = {k: bcb(c) for k, c in BCB.items()}
    ate = serie["usd"].dropna().index.max()
    meses = pd.period_range(INICIO, ate, freq="M").strftime("%Y-%m")

    def lista(s, casas=4):
        s = s.reindex(meses)
        return [None if pd.isna(v) else round(float(v), casas) for v in s]

    pib = bcb(7326, inicio=1990)
    dados = {
        "DADOS_ATE": ate,
        "BCB_START": INICIO,
        "BCB": {k: lista(v, 4 if k == "usd" else 2) for k, v in serie.items()},
        "PIB": {k[:4]: round(float(v), 2) for k, v in pib.items()},
        "MK": {k: lista(yahoo(t), 0 if k == "ibov" else 4) for k, t in MERCADO.items()},
        "FX": {k: lista(yahoo(t)) for k, t in MOEDAS.items()},
        "EMP": {t: lista(yahoo(t + ".SA"), 3) for t in EMPRESAS},
    }
    with open("dados.js", "w", encoding="utf-8") as f:
        f.write(f"// Gerado por fetch_data.py em {date.today():%d/%m/%Y}\n")
        for nome, valor in dados.items():
            f.write(f"const {nome}={json.dumps(valor, ensure_ascii=False, separators=(',', ':'))};\n")
    print(f"dados.js atualizado: {INICIO} a {ate}")


if __name__ == "__main__":
    main()
