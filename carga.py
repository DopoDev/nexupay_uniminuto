"""Prueba de carga simple, sin instalar nada (solo Python 3).

Uso:  python carga.py https://TU-APP.azurewebsites.net 600
      (URL de tu app y número total de solicitudes)
"""
import json
import random
import statistics
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = sys.argv[1].rstrip("/")
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 600


def una_solicitud(i):
    if i % 10 == 0:
        url, data = f"{BASE}/api/lento", None
    elif i % 15 == 0:
        url, data = f"{BASE}/api/error", None
    else:
        url = f"{BASE}/api/pagos"
        data = json.dumps({"monto": random.randint(1000, 6000000),
                           "comercio": f"Comercio {i % 20}"}).encode()
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            codigo = r.status
    except urllib.error.HTTPError as e:
        codigo = e.code
    except Exception:
        codigo = 0
    return url.rsplit("/", 1)[-1], codigo, (time.perf_counter() - inicio) * 1000


inicio = time.time()
with ThreadPoolExecutor(max_workers=20) as pool:
    resultados = list(pool.map(una_solicitud, range(TOTAL)))
duracion = time.time() - inicio

pagos = sorted(ms for ep, c, ms in resultados if ep == "pagos" and c == 200)
errores = sum(1 for _, c, _ in resultados if c >= 500 or c == 0)
print(f"Solicitudes: {TOTAL} en {duracion:.1f} s ({TOTAL / duracion:.1f} por segundo)")
print(f"Errores 5xx o de red: {errores} ({100 * errores / TOTAL:.1f} %)")
if pagos:
    p95 = pagos[int(len(pagos) * 0.95) - 1]
    print(f"/api/pagos -> mediana {statistics.median(pagos):.0f} ms, p95 {p95:.0f} ms")
