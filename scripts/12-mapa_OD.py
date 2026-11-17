import pandas as pd
from pathlib import Path
import folium
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CARGAR DATOS
# =========================

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

actividad_geo = pd.read_csv("data/processed/actividad_estaciones_geo.csv")


# =========================
# CÁLCULO DE RUTAS
# =========================

rutas = (
    df
    .groupby(
        [
            "start_station_number",
            "end_station_number"
        ]
    )
    .size()
    .reset_index(name="viajes")
)

rutas = rutas[
    rutas["start_station_number"]
    !=
    rutas["end_station_number"]
]


# =========================
# FILTRADO DE RUTAS PRINCIPALES
# =========================

rutas_top = rutas[
    rutas["viajes"] >= 1500
].copy()

coords = actividad_geo[
    [
        "id_estacion",
        "lat",
        "lon",
        "estacion"
    ]
].copy()


rutas_top = rutas_top.merge(
    coords,
    left_on="start_station_number",
    right_on="id_estacion",
    how="left"
)

rutas_top = rutas_top.rename(
    columns={
        "lat": "lat_inicio",
        "lon": "lon_inicio",
        "estacion": "estacion_inicio"
    }
).drop(columns="id_estacion")


# =========================
# INCORPORAR COORDENADAS
# =========================

rutas_top = rutas_top.merge(
    coords,
    left_on="end_station_number",
    right_on="id_estacion",
    how="left"
)

rutas_top = rutas_top.rename(
    columns={
        "lat": "lat_fin",
        "lon": "lon_fin",
        "estacion": "estacion_fin"
    }
).drop(columns="id_estacion")


# =========================
# COMPROBACIONES
# =========================

print("\nRutas más frecuentes:")
print(
    rutas_top[
        [
            "estacion_inicio",
            "estacion_fin",
            "viajes"
        ]
    ].head()
)

columnas_coordenadas = [
    "lat_inicio",
    "lon_inicio",
    "lat_fin",
    "lon_fin"
]

if rutas_top[columnas_coordenadas].isna().any().any():
    raise ValueError(
        "Hay rutas sin coordenadas de origen o destino."
    )

print("Comprobación de coordenadas: correcta.")

print(
    f"\nRutas representadas: {len(rutas_top)}"
)

print(
    f"Umbral mínimo: {rutas_top['viajes'].min():,} viajes"
)

# =========================
# EXPORTACIÓN
# =========================

Path(
    "data/processed/"
).mkdir(
    parents=True,
    exist_ok=True
)

rutas_top.to_csv(
    "data/processed/rutas_top_geo.csv",
    index=False
)

# =========================
# CREACIÓN DEL MAPA
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

for _, row in rutas_top.iterrows():

    # Color según intensidad
    if row["viajes"] >= 4000:
        color = "red"

    elif row["viajes"] >= 3000:
        color = "orange"

    elif row["viajes"] >= 2000:
        color = "gold"

    else:
        color = "royalblue"

    folium.PolyLine(
        locations=[
            [
                float(str(row["lat_inicio"]).replace(",", ".")),
                float(str(row["lon_inicio"]).replace(",", "."))
            ],
            [
                float(str(row["lat_fin"]).replace(",", ".")),
                float(str(row["lon_fin"]).replace(",", "."))
            ]
        ],

        weight=max(
            row["viajes"] / 700,
            2
        ),

        color=color,

        opacity=1,

        tooltip=(
            f"{row['estacion_inicio']} → "
            f"{row['estacion_fin']}<br>"
            f"Viajes: {row['viajes']:,}"
        )

    ).add_to(mapa)


# =========================
# MARCADORES DE ESTACIONES Y LEYENDA
# =========================

for _, row in coords.iterrows():

    folium.CircleMarker(
        location=[
            float(str(row["lat"]).replace(",", ".")),
            float(str(row["lon"]).replace(",", "."))
        ],
        radius=4,
        color="black",
        fill=True,
        fill_color="white",
        fill_opacity=1,
        tooltip=row["estacion"]
    ).add_to(mapa)


legend = """
<div style="position: fixed;
bottom: 40px;
left: 40px;
background: white;
padding: 8px;
border:1px solid black;
z-index:9999;">

<b>Viajes</b><br>
🟥 ≥ 4000<br>
🟧 ≥ 3000<br>
🟨 ≥ 2000<br>
🟦 ≥ 1500

</div>
"""

mapa.get_root().html.add_child(folium.Element(legend))


# =========================
# GUARDAR MAPA
# =========================

Path(
    "outputs/estaciones"
).mkdir(
    parents=True,
    exist_ok=True
)

mapa.save(
    "outputs/estaciones/mapa_OD.html"
)

print(
    "\nMapa OD generado correctamente."
)