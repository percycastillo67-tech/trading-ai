from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Trading AI Running"}

@app.post("/trade")
def trade(data: dict):
    activos = data.get("activos", ["AAPL"])
    timeframe = data.get("timeframe", "1mo")
    results = []
    for acc in activos:
        df = yf.download(acc, period=timeframe)["Close"]
        precio = float(df.iloc[-1])
        pred = float(df.mean())
        if pred > precio * 1.02:
            senal = "BUY"
        elif pred < precio * 0.98:
            senal = "SELL"
        else:
            senal = "HOLD"
        results.append({
            "activo": acc,
            "precio": precio,
            "pred": pred,
            "senal": senal
        })
    return results
@app.get("/monitor")
def monitor():

    activos = ["AAPL", "MSFT"]

    resultados = []

    for acc in activos:

        df = yf.download(acc, period="1mo")["Close"]

        precio = float(df.iloc[-1])
        pred = float(df.mean())

        if pred > precio * 1.02:
            senal = "BUY"
        elif pred < precio * 0.98:
            senal = "SELL"
        else:
            senal = "HOLD"

        resultados.append(f"{acc}: {senal}")

    print(resultados)  # para ver logs

    return resultados
