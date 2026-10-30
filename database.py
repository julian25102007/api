import json
import os

DB_FILE = "series_db.json"

def cargar_datos():
    if not os.path.exists(DB_FILE):
        datos_iniciales = [
            {
                "id": "1",
                "titulo": "Breaking Bad",
                "genero": "Drama",
                "temporadas_totales": 5,
                "temporadas_vistas": 5
            },
            {
                "id": "2",
                "titulo": "Stranger Things",
                "genero": "Ciencia ficción",
                "temporadas_totales": 4,
                "temporadas_vistas": 2
            },
            {
                "id": "3",
                "titulo": "The Office",
                "genero": "Comedia",
                "temporadas_totales": 9,
                "temporadas_vistas": 0
            },
            {
                "id": "4",
                "titulo": "Dark",
                "genero": "Misterio",
                "temporadas_totales": 3,
                "temporadas_vistas": 0
            },
            {
                "id": "5",
                "titulo": "Black Mirror",
                "genero": "Ciencia ficción",
                "temporadas_totales": 6,
                "temporadas_vistas": 1
            }
        ]
        guardar_datos(datos_iniciales)
        return datos_iniciales
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_datos(series):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=4)