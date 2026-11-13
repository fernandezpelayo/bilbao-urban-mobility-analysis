import pandas as pd

df = pd.read_csv(
    "data/raw/Viajes_Bilbaobizi_2021_2025.csv.gz",
    sep=";",
    compression="gzip"
)

df["start_time"] = pd.to_datetime(df["start_time"])
df["end_time"] = pd.to_datetime(df["end_time"])

# SOLO 2021
df = df[
    (df["start_time"] >= "2021-01-01") &
    (df["start_time"] < "2022-01-01")
]

# Duraciones válidas
df = df[
    (df["duration"] >= 2) &
    (df["duration"] <= 180)
]

df["air_distance_in_km"] = (
    df["air_distance_in_km"]
    .str.replace(",", ".", regex=False)
)

df["air_distance_in_km"] = pd.to_numeric(
    df["air_distance_in_km"],
    errors="coerce"
)

df["hora"] = df["start_time"].dt.hour
df["dia_semana"] = df["start_time"].dt.day_name()
df["fecha"] = df["start_time"].dt.normalize()

df.to_csv(
    "data/processed/movilidad_limpia.csv.gz",
    index=False,
    compression="gzip"
)