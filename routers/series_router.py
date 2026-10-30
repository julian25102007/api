from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.serie_schema import Serie, SerieCreate, EstadoSerie
from database import cargar_datos, guardar_datos
from services.serie_service import calcular_estado
import uuid

router = APIRouter(prefix="/series", tags=["Series"])

@router.get("", response_model=List[Serie])
def obtener_series(filtro: Optional[EstadoSerie] = None):
    series = cargar_datos()
    resultado = []
    
    for s in series:
        estado = calcular_estado(s["temporadas_vistas"], s["temporadas_totales"])
        serie_obj = Serie(
            id=s["id"],
            titulo=s["titulo"],
            genero=s["genero"],
            temporadas_totales=s["temporadas_totales"],
            temporadas_vistas=s["temporadas_vistas"],
            estado=estado
        )
        if filtro is None or estado == filtro:
            resultado.append(serie_obj)
            
    return resultado

@router.post("", response_model=Serie, status_code=status.HTTP_201_CREATED)
def crear_serie(serie_in: SerieCreate):
    series = cargar_datos()
    
    nueva_serie = {
        "id": str(uuid.uuid4()),
        "titulo": serie_in.titulo,
        "genero": serie_in.genero,
        "temporadas_totales": serie_in.temporadas_totales,
        "temporadas_vistas": 0
    }
    
    series.append(nueva_serie)
    guardar_datos(series)
    
    estado = calcular_estado(0, nueva_serie["temporadas_totales"])
    return Serie(
        id=nueva_serie["id"],
        titulo=nueva_serie["titulo"],
        genero=nueva_serie["genero"],
        temporadas_totales=nueva_serie["temporadas_totales"],
        temporadas_vistas=0,
        estado=estado
    )

@router.patch("/{serie_id}/avanzar", response_model=Serie)
def modificar_avance(serie_id: str, incrementar: bool = True):
    series = cargar_datos()
    serie_encontrada = None
    
    for s in series:
        if s["id"] == serie_id:
            serie_encontrada = s
            break
            
    if not serie_encontrada:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
        
    if incrementar:
        if serie_encontrada["temporadas_vistas"] < serie_encontrada["temporadas_totales"]:
            serie_encontrada["temporadas_vistas"] += 1
    else:
        if serie_encontrada["temporadas_vistas"] > 0:
            serie_encontrada["temporadas_vistas"] -= 1
            
    guardar_datos(series)
    
    estado = calcular_estado(serie_encontrada["temporadas_vistas"], serie_encontrada["temporadas_totales"])
    return Serie(
        id=serie_encontrada["id"],
        titulo=serie_encontrada["titulo"],
        genero=serie_encontrada["genero"],
        temporadas_totales=serie_encontrada["temporadas_totales"],
        temporadas_vistas=serie_encontrada["temporadas_vistas"],
        estado=estado
    )

@router.delete("/{serie_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_serie(serie_id: str):
    series = cargar_datos()
    nuevas_series = [s for s in series if s["id"] != serie_id]
    
    if len(nuevas_series) == len(series):
        raise HTTPException(status_code=404, detail="Serie no encontrada")
        
    guardar_datos(nuevas_series)
    return None