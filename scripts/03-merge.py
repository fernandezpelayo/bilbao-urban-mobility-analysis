import pandas as pd


# Cargar datasets
mov = pd.read_csv(
    "data/processed/movilidad_limpia.csv.gz",
    compression="gzip",
    low_memory=False
)

clima = pd.read_csv(
    "data/raw/clima_2021.csv",
    low_memory=False
)


# Convertir fechas
mov["fecha"] = pd.to_datetime(mov["fecha"])
clima["fecha"] = pd.to_datetime(clima["fecha"])


# Limpiar variables meteorológicas
columnas_numericas = [
    "tmed",
    "prec",
    "tmin",
    "tmax",
    "velmedia",
    "racha",
    "sol",
    "presMax",
    "presMin"
]

# AEMET usa "Ip" para precipitación inapreciable
clima["prec"] = clima["prec"].replace("Ip", "0")


for col in columnas_numericas:

    clima[col] = (
        clima[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    clima[col] = pd.to_numeric(
        clima[col],
        errors="coerce"
    )


# Merge
df_final = mov.merge(
    clima,
    on="fecha",
    how="left",
    validate="many_to_one"
)

# Guardar
df_final.to_csv(
    "data/processed/df_final.csv.gz",
    index=False,
    compression="gzip"
)


# Comprobaciones
print("Shape:")
print(df_final.shape)

print("\nFechas:")
print(df_final["fecha"].min())
print(df_final["fecha"].max())

print("\nNulos clima:")
print(df_final["tmed"].isna().sum())