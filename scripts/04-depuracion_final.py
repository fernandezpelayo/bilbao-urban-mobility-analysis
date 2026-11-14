import pandas as pd


# Cargar dataset unido
df = pd.read_csv(
    "data/processed/df_final.csv.gz",
    compression="gzip",
    low_memory=False
)


# Estaciones internas del sistema
estaciones_excluir = [
    "BALANCEO",
    "ESTACIÓN PARA PRUEBAS",
    "BICICLETAS CUADRO DESMONTADO",
    "TALLER - Bicis defectuosas",
    "TALLER - Bicis listas"
]


# Eliminar viajes asociados a ellas
df = df[
    ~df["start_street1"].isin(estaciones_excluir)
]

df = df[
    ~df["end_street1"].isin(estaciones_excluir)
]


# Guardar dataset final
df.to_csv(
    "data/processed/df_final_limpio.csv.gz",
    index=False,
    compression="gzip"
)


# Comprobaciones
print("=" * 40)
print("DATASET FINAL")
print("=" * 40)

print("\nViajes:")
print(len(df))

print("\nEstaciones origen:")
print(df["start_street1"].nunique())

print("\nEstaciones destino:")
print(df["end_street1"].nunique())

print("\nListado estaciones:")
print(sorted(df["start_street1"].unique()))