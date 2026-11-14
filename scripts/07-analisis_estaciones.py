import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


Path("outputs/analisis_estaciones").mkdir(
    parents=True,
    exist_ok=True
)

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

top_origen = (
    df["start_street1"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10,5))

top_origen.sort_values().plot(kind="barh")

plt.title("Top 10 estaciones origen")
plt.xlabel("Número de viajes")
plt.ylabel("")

plt.tight_layout()

plt.savefig(
    "outputs/analisis_estaciones/top_estaciones_origen.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


top_destino = (
    df["end_street1"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10,5))

top_destino.sort_values().plot(kind="barh")

plt.title("Top 10 estaciones destino")
plt.xlabel("Número de viajes")
plt.ylabel("")

plt.tight_layout()

plt.savefig(
    "outputs/analisis_estaciones/top_estaciones_destino.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


print("\nTOP ORIGEN")
print(top_origen)

print("\nTOP DESTINO")
print(top_destino)

origen = (
    df["start_street1"]
    .value_counts()
    .rename("salidas")
)

destino = (
    df["end_street1"]
    .value_counts()
    .rename("entradas")
)

balance = pd.concat(
    [origen, destino],
    axis=1
).fillna(0)

balance["balance"] = (
    balance["entradas"]
    - balance["salidas"]
)

print(
    balance.sort_values(
        "balance",
        ascending=False
    ).head(10)
)

print(
    balance.sort_values(
        "balance",
        ascending=True
    ).head(10)
)

balance_top = (
    balance["balance"]
    .sort_values()
)

plt.figure(figsize=(12,6))

balance_top.plot(kind="barh")

plt.title("Balance de viajes por estación")
plt.xlabel("Entradas - Salidas")
plt.ylabel("")

plt.tight_layout()

plt.savefig(
    "outputs/analisis_estaciones/balance_estaciones.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


estaciones = sorted(df["start_street1"].unique())

print("Número de estaciones:")
print(len(estaciones))

print("\nListado completo:")
for e in estaciones:
    print(e)


print(
    sorted(
        df["end_street1"].unique()
    )
)

