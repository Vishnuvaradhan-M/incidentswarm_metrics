import random
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

_incident_active = False
_incident_start  = 0.0

@app.post("/trigger")
def trigger():
    global _incident_active, _incident_start
    _incident_active = True
    _incident_start  = time.time()
    return {"status": "incident triggered"}

@app.post("/reset")
def reset():
    global _incident_active
    _incident_active = False
    return {"status": "reset"}

@app.get("/metrics")
def get_metrics():
    elapsed = time.time() - _incident_start if _incident_active else 0
    if _incident_active and elapsed < 300:
        cpu = round(random.uniform(88.0, 97.0), 1)
        mem = round(random.uniform(87.0, 94.0), 1)
        err = round(random.uniform(18.0, 28.0), 1)
        rsp = round(random.uniform(2800, 4200), 0)
        pool = random.randint(95, 100)
    else:
        global _incident_active
        _incident_active = False
        cpu = round(random.uniform(12.0, 22.0), 1)
        mem = round(random.uniform(35.0, 48.0), 1)
        err = round(random.uniform(0.5, 1.8), 1)
        rsp = round(random.uniform(95, 145), 0)
        pool = random.randint(8, 15)
    return {
        "service": "checkout-service",
        "timestamp": "live",
        "cpu_percent": cpu,
        "memory_percent": mem,
        "error_rate_percent": err,
        "response_time_ms": rsp,
        "normal_response_time_ms": 120,
        "requests_per_second": round(random.uniform(400, 900), 0),
        "failed_requests": int(err * 10),
        "db_connection_pool_used": pool,
        "db_connection_pool_max": 100,
    }

@app.get("/health")
def health():
    return {"status": "ok"}
