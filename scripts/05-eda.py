import pandas as pd

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

print("=" * 50)
print("INFORMACIÓN GENERAL")
print("=" * 50)

print("\nViajes totales:")
print(len(df))

print("\nPeriodo:")
print(df["fecha"].min())
print(df["fecha"].max())

print("\nEstaciones origen únicas:")
print(df["start_station_number"].nunique())

print("\nEstaciones destino únicas:")
print(df["end_station_number"].nunique())

print("\nDuración media (min):")
print(round(df["duration"].mean(), 2))

print("\nDistancia media (km):")
print(round(df["air_distance_in_km"].mean(), 2))


print("\n" + "=" * 50)
print("DURACIÓN")
print("=" * 50)

print(df["duration"].describe())


print("\n" + "=" * 50)
print("DISTANCIA")
print("=" * 50)

print(df["air_distance_in_km"].describe())


print("\n" + "=" * 50)
print("VIAJES POR DÍA")
print("=" * 50)

print(
    df.groupby("fecha")
      .size()
      .describe()
)