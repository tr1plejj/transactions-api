import asyncio
import time
from contextlib import asynccontextmanager

import psutil
from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, Counter, Gauge, Histogram

from src.routers import all_routers


@asynccontextmanager
async def lifecycle(a: FastAPI):
    asyncio.create_task(update_simple_metrics())
    yield


app = FastAPI(lifespan=lifecycle)
app.include_router(all_routers)

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

ERROR_COUNT = Counter(
    "fastapi_errors_total", "Total application errors", ["error_type", "endpoint"]
)

ACTIVE_REQUESTS = Gauge(
    "fastapi_active_requests", "Number of currently active requests"
)

CPU_GAUGE = Gauge("system_cpu_percent", "CPU usage percentage")
MEMORY_GAUGE = Gauge("system_memory_percent", "Memory usage percentage")
DISK_GAUGE = Gauge("system_disk_percent", "Disk usage percentage")

REQUEST_DURATION = Histogram(
    "fastapi_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint", "status_code"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)


async def update_simple_metrics():
    while True:
        CPU_GAUGE.set(psutil.cpu_percent())

        memory = psutil.virtual_memory()
        MEMORY_GAUGE.set(memory.percent)

        disk = psutil.disk_usage("/")
        DISK_GAUGE.set(disk.percent)

        await asyncio.sleep(5)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    ACTIVE_REQUESTS.inc()
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        ERROR_COUNT.labels(error_type=type(e).__name__, endpoint=request.url.path).inc()
        raise
    finally:
        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=status_code,
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method, endpoint=request.url.path, status_code=status_code
        ).observe(duration)

        ACTIVE_REQUESTS.dec()
    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
