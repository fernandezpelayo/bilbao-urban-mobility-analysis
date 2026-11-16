import pandas as pd

df = pd.read_csv(
    "data/raw/Viajes_Bilbaobizi_2021_2025.csv.gz",
    sep=";",
    compression="gzip"
)

# Comprobar columnas necesarias
columnas_necesarias = [
    "uid",
    "start_time",
    "end_time",
    "duration",
    "air_distance_in_km",
    "start_station_number",
    "end_station_number"
]

faltantes = set(columnas_necesarias) - set(df.columns)

if faltantes:
    raise ValueError(f"Faltan columnas obligatorias: {faltantes}")

filas_iniciales = len(df)
print(f"Registros iniciales: {filas_iniciales}")

df["start_time"] = pd.to_datetime(df["start_time"])
df["end_time"] = pd.to_datetime(df["end_time"])

# SOLO 2021
df = df[
    (df["start_time"] >= "2021-01-01") &
    (df["start_time"] < "2022-01-01")
]

filas_2021 = len(df)
print(f"Registros de 2021: {filas_2021}")
print(f"Registros descartados por fecha: {filas_iniciales - filas_2021}")

# Duraciones válidas
df = df[
    (df["duration"] >= 2) &
    (df["duration"] <= 180)
]

filas_duracion = len(df)
print(f"Registros con duración válida: {filas_duracion}")
print(f"Registros descartados por duración: {filas_2021 - filas_duracion}")

# Comprobar viajes duplicados
duplicados = df["uid"].duplicated().sum()

if duplicados > 0:
    raise ValueError(f"Se han encontrado {duplicados} viajes duplicados.")

print("Comprobación de duplicados: correcta.")

# Limpiar y convertir distancias
distancia_original = df["air_distance_in_km"].copy()

df["air_distance_in_km"] = (
    df["air_distance_in_km"]
    .str.replace(",", ".", regex=False)
)

df["air_distance_in_km"] = pd.to_numeric(
    df["air_distance_in_km"],
    errors="coerce"
)

distancias_invalidas = (
    distancia_original.notna() &
    df["air_distance_in_km"].isna()
).sum()

print(f"Distancias que no se han podido convertir: {distancias_invalidas}")
print(f"Distancias sin dato: {df['air_distance_in_km'].isna().sum()}")

df["hora"] = df["start_time"].dt.hour
df["dia_semana"] = df["start_time"].dt.day_name()
df["fecha"] = df["start_time"].dt.normalize()

df.to_csv(
    "data/processed/movilidad_limpia.csv.gz",
    index=False,
    compression="gzip"
)