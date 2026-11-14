
import pandas as pd
import folium
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CARGAR ACTIVIDAD
# =========================

actividad = pd.read_csv(
    "data/processed/actividad_estaciones.csv"
)

coords = pd.read_csv(
    "data/raw/estaciones_Bilbaobizi.csv",
    sep=";", low_memory=False
)

# =========================
# CARGAR Y LIMPIAR COORDENADAS
# =========================

coords = coords[
    [
        "#id",
        "name",
        "lat",
        "lon"
    ]
].copy()

coords = coords.rename(
    columns={
        "#id": "numero",
        "name": "nombre_coord"
    }
)

coords = (
    coords[
        coords["numero"] <= 43
    ]
    .copy()
)

# =========================
# MERGE
# =========================

actividad["numero"] = (
    actividad["estacion"]
    .str.extract(r"(\d+)")
    .astype(int)
)

mapa_df = actividad.merge(
    coords,
    on="numero",
    how="left"
)

mapa_df.to_csv(
    "data/processed/actividad_estaciones_geo.csv",
    index=False
)


print("\n" + "="*50)
print("COMPROBACIÓN DE COORDENADAS")
print("="*50)

print(
    mapa_df[
        ["numero", "estacion", "lat", "lon"]
    ].head()
)

print(
    f"\nLatitudes faltantes: {mapa_df['lat'].isna().sum()}"
)

print(
    f"Longitudes faltantes: {mapa_df['lon'].isna().sum()}"
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

mapa = folium.Map(
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
).add_to(mapa)


for _, row in mapa_df.iterrows():

    folium.CircleMarker(
        location=[
            float(str(row["lat"]).replace(",", ".")),
            float(str(row["lon"]).replace(",", "."))
        ],
        radius=max(
            row["actividad_total"] / 4000,
            3
        ),

        tooltip=(
            f"{row['estacion']}<br>"
            f"Total viajes: {row['actividad_total']:,}"
        ),

        popup=(
            f"<b>{row['estacion']}</b><br>"
            f"🚲 Salidas: {row['salidas']:,}<br>"
            f"📍 Llegadas: {row['llegadas']:,}<br>"
            f"📊 Total movimientos: {row['actividad_total']:,}"
        ),

        fill=True
    ).add_to(mapa)


# =========================
# GUARDAR HTML
# =========================

Path(
    "outputs/estaciones"
).mkdir(
    parents=True,
    exist_ok=True
)

mapa.save(
    "outputs/estaciones/mapa_actividad_estaciones.html"
)

print(
    "\nMapa de actividad generado correctamente."
)