import pandas as pd
import folium
from folium.plugins import HeatMap
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CARGAR DATOS
# =========================

mapa_df = pd.read_csv(
   "data/processed/actividad_estaciones_geo.csv"
)

# =========================
# CREAR MAPA
# =========================

carto_api_key = os.getenv("CARTO_API_KEY")

if not carto_api_key:
    raise ValueError(
        "No se ha encontrado CARTO_API_KEY. "
        "Configura tu clave de CARTO en el archivo .env."
    )

heatmap = folium.Map(
    location=[43.2630, -2.9350],
    zoom_start=13,
    tiles=None
)

folium.TileLayer(
    tiles=f"https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png?key={carto_api_key}",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    name="CartoDB Positron",
    subdomains="abcd",
    max_zoom=20
).add_to(heatmap)


# =========================
# PREPARAR DATOS HEATMAP
# =========================

for columna in ["lat", "lon"]:
    mapa_df[columna] = pd.to_numeric(
        mapa_df[columna].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )

if mapa_df[["lat", "lon"]].isna().any().any():
    raise ValueError("Hay coordenadas ausentes o no numéricas en el dataset geográfico.")


heat_data = []

for _, row in mapa_df.iterrows():

    heat_data.append(
        [
            row["lat"],
            row["lon"],
            row["actividad_total"]
        ]
    )

# =========================
# GENERAR HEATMAP
# =========================

HeatMap(
    heat_data,
    radius=30,
    blur=25,
    max_zoom=15
).add_to(heatmap)


# =========================
# GUARDAR HTML
# =========================

Path(
    "outputs/estaciones"
).mkdir(
    parents=True,
    exist_ok=True
)

heatmap.save(
    "outputs/estaciones/heatmap_estaciones.html"
)

print(
    "\nHeatMap generado correctamente."
)
