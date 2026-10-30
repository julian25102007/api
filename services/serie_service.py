from models.serie_model import EstadoSerie

def calcular_estado(temporadas_vistas: int, temporadas_totales: int) -> EstadoSerie:
    """Calcula el estado actual de una serie según sus temporadas vistas."""
    if temporadas_vistas == 0:
        return EstadoSerie.POR_VER
    elif temporadas_vistas >= temporadas_totales:
        return EstadoSerie.TERMINADA
    else:
        return EstadoSerie.VIENDO