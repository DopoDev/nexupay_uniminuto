"""API de demostración de NexoPay para la prueba de campo en Azure App Service."""
import os
import random
import time

# Telemetría hacia Application Insights. App Service define esta variable
# automáticamente cuando Application Insights está habilitado en la app.
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

VERSION = "1.0.0"

app = FastAPI(title="NexoPay API demo", version=VERSION)


class Pago(BaseModel):
    monto: float = Field(gt=0, description="Monto en pesos colombianos")
    comercio: str = Field(min_length=1)


def puntaje_fraude(monto: float) -> float:
    """Puntaje simulado entre 0 y 1; montos altos tienen más riesgo."""
    base = min(monto / 5_000_000, 1.0) * 0.6
    return round(min(base + random.uniform(0, 0.4), 1.0), 3)


@app.get("/health")
def health():
    return {"estado": "ok"}


@app.get("/api/version")
def version():
    return {"servicio": "nexopay-api", "version": VERSION}


@app.post("/api/pagos")
def autorizar_pago(pago: Pago):
    time.sleep(random.uniform(0.02, 0.15))  # simula consulta a base de datos
    score = puntaje_fraude(pago.monto)
    if score >= 0.85:
        decision = "rechazado"
    elif score >= 0.6:
        decision = "revision"
    else:
        decision = "aprobado"
    return {"comercio": pago.comercio, "monto": pago.monto,
            "score_fraude": score, "decision": decision}


@app.get("/api/lento")
def lento():
    time.sleep(random.uniform(0.8, 1.5))  # dependencia lenta simulada
    return {"mensaje": "respuesta lenta"}


@app.get("/api/error")
def error():
    if random.random() < 0.5:
        raise HTTPException(status_code=500, detail="Falla simulada del proveedor")
    return {"mensaje": "esta vez funcionó"}
