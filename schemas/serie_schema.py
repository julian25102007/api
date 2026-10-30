from pydantic import BaseModel, Field
from models.serie_model import EstadoSerie

class SerieBase(BaseModel):
    titulo: str = Field(..., min_length=1, description="Título de la serie")
    genero: str = Field(..., min_length=1, description="Género de la serie")
    temporadas_totales: int = Field(..., gt=0, description="Número total de temporadas")

class SerieCreate(SerieBase):
    pass

class Serie(SerieBase):
    id: str
    temporadas_vistas: int = Field(0, ge=0, description="Temporadas ya vistas")
    estado: EstadoSerie = EstadoSerie.POR_VER