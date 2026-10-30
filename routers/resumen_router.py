from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.serie_model import SerieModel, EstadoSerie

router = APIRouter(
    prefix="/resumen",
    tags=["Resumen"]
)

@router.get("/")
def obtener_resumen(db: Session = Depends(get_db)):
    series = db.query(SerieModel).all()
    
    total_series = len(series)
    total_temporadas_vistas = 0
    total_temporadas_totales = 0
    por_ver = 0
    viendo = 0
    terminadas = 0
    
    for s in series:
        total_temporadas_vistas += s.temporadas_vistas
        total_temporadas_totales += s.temporadas_totales
        
        # Calcular estado de cada serie
        if s.temporadas_vistas == 0:
            por_ver += 1
        elif s.temporadas_vistas >= s.temporadas_totales:
            terminadas += 1
        else:
            viendo += 1
            
    return {
        "total_series": total_series,
        "total_temporadas_vistas": total_temporadas_vistas,
        "total_temporadas_totales": total_temporadas_totales,
        "por_ver": por_ver,
        "viendo":viendo,
        "terminadas": terminadas
    }