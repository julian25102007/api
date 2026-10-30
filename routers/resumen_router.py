from fastapi import APIRouter
from pydantic import BaseModel
from database import cargar_datos

router = APIRouter(prefix="/resumen", tags=["Resumen"])

class ResumenResponse(BaseModel):
    porcentaje_avance: float
    temporadas_vistas_totales: int
    temporadas_totales_biblioteca: int
    series_terminadas: int
    series_totales: int

@router.get("", response_model=ResumenResponse)
def obtener_resumen():
    series = cargar_datos()
    
    if not series:
        return ResumenResponse(
            porcentaje_avance=0.0,
            temporadas_vistas_totales=0,
            temporadas_totales_biblioteca=0,
            series_terminadas=0,
            series_totales=0
        )
        
    t_vistas = sum(s["temporadas_vistas"] for s in series)
    t_totales = sum(s["temporadas_totales"] for s in series)
    
    series_term = sum(1 for s in series if s["temporadas_vistas"] == s["temporadas_totales"])
    series_tot = len(series)
    
    porcentaje = (t_vistas / t_totales * 100) if t_totales > 0 else 0.0
    
    return ResumenResponse(
        porcentaje_avance=round(porcentaje, 2),
        temporadas_vistas_totales=t_vistas,
        temporadas_totales_biblioteca=t_totales,
        series_terminadas=series_term,
        series_totales=series_tot
    )