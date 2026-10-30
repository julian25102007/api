import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.serie_model import SerieModel, EstadoSerie
from schemas.serie_schema import Serie, SerieCreate

router = APIRouter(
    prefix="/series",
    tags=["Series"]
)

def calcular_estado(vistas: int, totales: int) -> str:
    if vistas == 0:
        return EstadoSerie.POR_VER
    elif vistas >= totales:
        return EstadoSerie.TERMINADA
    else:
        return EstadoSerie.VIENDO

@router.get("/", response_model=list[Serie])
def listar_series(filtro: Optional[str] = None, db: Session = Depends(get_db)):
    series_db = db.query(SerieModel).all()
    resultado = []
    
    for s in series_db:
        estado = calcular_estado(s.temporadas_vistas, s.temporadas_totales)
        
        # Si hay un filtro por estado, lo aplicamos
        if filtro is None or estado == filtro:
            serie_obj = Serie(
                id=s.id,
                titulo=s.titulo,
                genero=s.genero,
                temporadas_totales=s.temporadas_totales,
                temporadas_vistas=s.temporadas_vistas,
                estado=estado
            )
            resultado.append(serie_obj)
            
    return resultado

@router.post("", response_model=Serie, status_code=status.HTTP_201_CREATED)
def crear_serie(serie_in: SerieCreate, db: Session = Depends(get_db)):
    nuevo_id = str(uuid.uuid4())
    
    nueva_serie = SerieModel(
        id=nuevo_id,
        titulo=serie_in.titulo,
        genero=serie_in.genero,
        temporadas_totales=serie_in.temporadas_totales,
        temporadas_vistas=0
    )
    
    db.add(nueva_serie)
    db.commit()
    db.refresh(nueva_serie)
    
    estado = calcular_estado(0, nueva_serie.temporadas_totales)
    return Serie(
        id=nueva_serie.id,
        titulo=nueva_serie.titulo,
        genero=nueva_serie.genero,
        temporadas_totales=nueva_serie.temporadas_totales,
        temporadas_vistas=nueva_serie.temporadas_vistas,
        estado=estado
    )

@router.patch("/{serie_id}/avanzar", response_model=Serie)
def modificar_avance(serie_id: str, incrementar: bool = True, db: Session = Depends(get_db)):
    serie_encontrada = db.query(SerieModel).filter(SerieModel.id == serie_id).first()
    
    if not serie_encontrada:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
        
    if incrementar:
        if serie_encontrada.temporadas_vistas < serie_encontrada.temporadas_totales:
            serie_encontrada.temporadas_vistas += 1
    else:
        if serie_encontrada.temporadas_vistas > 0:
            serie_encontrada.temporadas_vistas -= 1
            
    db.commit()
    db.refresh(serie_encontrada)
    
    estado = calcular_estado(serie_encontrada.temporadas_vistas, serie_encontrada.temporadas_totales)
    return Serie(
        id=serie_encontrada.id,
        titulo=serie_encontrada.titulo,
        genero=serie_encontrada.genero,
        temporadas_totales=serie_encontrada.temporadas_totales,
        temporadas_vistas=serie_encontrada.temporadas_vistas,
        estado=estado
    )

@router.delete("/{serie_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_serie(serie_id: str, db: Session = Depends(get_db)):
    serie_encontrada = db.query(SerieModel).filter(SerieModel.id == serie_id).first()
    
    if not serie_encontrada:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
        
    db.delete(serie_encontrada)
    db.commit()
    return None