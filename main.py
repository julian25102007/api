import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.series_router import router as series_router
from routers.resumen_router import router as resumen_router

app = FastAPI(
    title="Biblioteca de Series API",
    version="1.0.0",
    description="API backend para la gestión de series y control de avance local."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(series_router, prefix="/api/v1")
app.include_router(resumen_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Biblioteca de Series 🚀"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.main.run("main:app", host="0.0.0.0", port=port, reload=True)