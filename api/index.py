"""
Bússola 2030 — API (FastAPI) + Site Frontend na Vercel.
Todas as rotas /api/... e páginas estáticas são atendidas aqui.
O código dos 5 agentes fica na pasta /backend.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from bussola_api.routers.bussola_router import router as bussola_router  # noqa: E402
from bussola_api.routers.analysis_router import router as analysis_router  # noqa: E402

app = FastAPI(
    title="Bússola 2030 API • Prisma Insights",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(bussola_router)
app.include_router(analysis_router)


@app.get("/health", tags=["Health Check"])
@app.get("/api/health", tags=["Health Check"])
def health():
    return {"status": "healthy", "service": "Bússola 2030 API"}


@app.get("/", tags=["Site"])
@app.get("/index.html", tags=["Site"])
def read_root():
    path = os.path.join(ROOT, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"status": "ok", "message": "index.html not found"}


@app.get("/bussola", tags=["Site"])
@app.get("/bussola.html", tags=["Site"])
def read_bussola():
    path = os.path.join(ROOT, "bussola.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"status": "ok", "message": "bussola.html not found"}


# Montar diretórios de recursos estáticos
for static_dir in ["css", "js", "assets", "vendor", "downloads"]:
    dir_path = os.path.join(ROOT, static_dir)
    if os.path.exists(dir_path):
        app.mount(f"/{static_dir}", StaticFiles(directory=dir_path), name=static_dir)
