from sqlalchemy import Column, String, Integer, Enum as SQLEnum
import enum
from database import Base

class EstadoSerie(str, enum.Enum):
    POR_VER = "Por ver"
    VIENDO = "Viendo"
    TERMINADA = "Terminada"

class SerieModel(Base):
    __tablename__ = "series"

    id = Column(String(36), primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    genero = Column(String(100), nullable=False)
    temporadas_totales = Column(Integer, nullable=False)
    temporadas_vistas = Column(Integer, default=0)