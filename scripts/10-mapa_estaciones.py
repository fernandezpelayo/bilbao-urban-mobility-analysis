
import pandas as pd
import folium
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CARGAR ACTIVIDAD
# =========================


actividad = pd.read_csv("data/processed/actividad_estaciones.csv")

coords = pd.read_csv(
    "data/raw/estaciones_Bilbaobizi.csv",
    sep=";",
    low_memory=False
)

# Seleccionar y preparar las coordenadas actuales
coords = coords[["#id", "name", "lat", "lon"]].copy()

coords = coords.rename(columns={
    "#id": "id_coord",
    "name": "nombre_coord"
})

coords["lat"] = pd.to_numeric(
    coords["lat"].astype(str).str.replace(",", ".", regex=False)
)

coords["lon"] = pd.to_numeric(
    coords["lon"].astype(str).str.replace(",", ".", regex=False)
)

# Correspondencia entre estaciones históricas y actuales
correspondencia = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    9: 8,
    10: 9,
    11: 10,
    12: 11,
    13: 12,
    14: 13,
    15: 14,
    16: 15,
    17: 16,
    18: 17,
    19: 18,
    20: 19,
    21: 20,
    22: 21,
    23: 22,
    24: 23,
    25: 24,
    26: 25,
    27: 26,
    28: 27,
    29: 28,
    30: 29,
    31: 30,
    32: 31,
    33: 32,
    34: 33,
    35: 34,
    36: 35,
    37: 36,
    38: 37,
    39: 38,
    40: 64,
    41: 40,
    42: 41,
    43: 42
}

# Obtener el número de estación histórica
actividad["numero"] = (
    actividad["estacion"]
    .str.extract(r"(\d+)")
    .astype(int)
)

# Asignar el identificador de la estación actual
actividad["id_coord"] = actividad["numero"].map(correspondencia)

# Incorporar las coordenadas actuales
mapa_df = actividad.merge(
    coords,
    on="id_coord",
    how="left"
)

# Coordenadas históricas de estaciones que ya no aparecen
coordenadas_historicas = {
    1: (43.28159, -2.96191),  # LEVANTE
    8: (43.26183, -2.94885)   # ZUNZUNEGUI
}

for numero, (lat, lon) in coordenadas_historicas.items():
    mapa_df.loc[mapa_df["numero"] == numero, "lat"] = lat
    mapa_df.loc[mapa_df["numero"] == numero, "lon"] = lon

# Comprobar las coordenadas asignadas
print("\nESTACIONES SIN COORDENADAS:")
print(
    mapa_df.loc[
        mapa_df["lat"].isna() | mapa_df["lon"].isna(),
        "estacion"
    ].tolist()
)

print("\nTOTAL DE ESTACIONES:")
print(len(mapa_df))

print("\nESTACIONES CON COORDENADAS:")
print(mapa_df[["estacion", "lat", "lon"]].notna().all(axis=1).sum())

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