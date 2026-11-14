import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# CARGA DE DATOS
# =========================

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

# =========================
# CÁLCULO DE INDICADORES POR ESTACIÓN
# =========================


salidas = (
    df
    .groupby(
        [
            "start_station_number",
            "start_street1"
        ]
    )
    ["uid"]
    .count()
    .reset_index()
    .rename(
        columns={
            "start_station_number": "id_estacion",
            "start_street1": "estacion",
            "uid": "salidas"
        }
    )
)


llegadas = (
    df
    .groupby(
        [
            "end_station_number",
            "end_street1"
        ]
    )
    ["uid"]
    .count()
    .reset_index()
    .rename(
        columns={
            "end_station_number": "id_estacion",
            "end_street1": "estacion",
            "uid": "llegadas"
        }
    )
)


actividad = (
    salidas
    .merge(
        llegadas,
        on=[
            "id_estacion",
            "estacion"
        ],
        how="outer"
    )
)

actividad = actividad.fillna(0)


actividad["actividad_total"] = (
    actividad["salidas"] +
    actividad["llegadas"]
)


actividad["balance"] = (
    actividad["llegadas"]
    - actividad["salidas"]
)

# =========================
# EXPORTACIÓN
# =========================

actividad.to_csv(
    "data/processed/actividad_estaciones.csv",
    index=False
)

ranking_estaciones = (
    actividad
    .sort_values(
        "actividad_total",
        ascending=False
    )
)


ranking_estaciones = ranking_estaciones.reset_index(drop=True)

ranking_estaciones.to_csv(
    "data/processed/ranking_estaciones.csv",
    index=False
)

# =========================
# RANKING DE ESTACIONES
# =========================

top10_salidas = (
    salidas
    .sort_values("salidas", ascending=False)
    .head(10)
)

top10_llegadas = (
    llegadas
    .sort_values("llegadas", ascending=False)
    .head(10)
)

top10_actividad = (
    actividad
    .sort_values("actividad_total", ascending=False)
    .head(10)
)


top10_receptoras = (
    actividad
    .sort_values("balance", ascending=False)
    .head(10)
)

top10_emisoras = (
    actividad
    .sort_values("balance")
    .head(10)
)


# =========================
# RESULTADOS
# =========================

print("\n" + "="*50)
print("TOP 10 ESTACIONES CON MÁS SALIDAS")
print("="*50)

print(top10_salidas)



print("\n" + "="*50)
print("TOP 10 ESTACIONES CON MÁS LLEGADAS")
print("="*50)


print(top10_llegadas)


print("\n" + "="*50)
print("TOP 10 ESTACIONES RECEPTORAS")
print("="*50)

print(top10_receptoras)


print("\n" + "="*50)
print("TOP 10 ESTACIONES EMISORAS")
print("="*50)

print(top10_emisoras)


print("\n" + "="*50)
print("TOP 10 ESTACIONES MÁS ACTIVAS")
print("="*50)

print(top10_actividad)


# =========================
# OBSERVACIONES
# =========================

print("\n" + "="*50)
print("OBSERVACIONES")
print("="*50)


print(
    f"\nEstación más activa: "
    f"{top10_actividad.iloc[0]['estacion']}"
)

print(
    f"Actividad total: "
    f"{top10_actividad.iloc[0]['actividad_total']:,}"
)

print(
    f"\nMayor balance positivo: "
    f"{top10_receptoras.iloc[0]['estacion']}"
)

print(
    f"Balance: "
    f"{top10_receptoras.iloc[0]['balance']:,}"
)

print(
    f"\nMayor balance negativo: "
    f"{top10_emisoras.iloc[0]['estacion']}"
)

print(
    f"Balance: "
    f"{top10_emisoras.iloc[0]['balance']:,}"
)



# =========================
# GRÁFICOS
# =========================


Path(
    "outputs/estaciones"
).mkdir(
    parents=True,
    exist_ok=True
)

plt.figure(figsize=(10,6))

plt.barh(
    top10_salidas["estacion"],
    top10_salidas["salidas"]
)

plt.title("Top 10 estaciones con mayor número de salidas")
plt.xlabel("Número de salidas")
plt.ylabel("")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "outputs/estaciones/top10_salidas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


plt.figure(figsize=(10,6))

plt.barh(
    top10_llegadas["estacion"],
    top10_llegadas["llegadas"]
)

plt.title("Top 10 estaciones con mayor número de llegadas")
plt.xlabel("Número de llegadas")
plt.ylabel("")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "outputs/estaciones/top10_llegadas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()



plt.figure(figsize=(10,6))

plt.barh(
    top10_actividad["estacion"],
    top10_actividad["actividad_total"]
)

plt.title("Top 10 estaciones con mayor actividad")
plt.xlabel("Viajes totales")
plt.ylabel("")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "outputs/estaciones/top10_actividad.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()



plt.figure(figsize=(10,6))

plt.barh(
    top10_receptoras["estacion"],
    top10_receptoras["balance"]
)

plt.title("Estaciones con mayor balance positivo")
plt.xlabel("Llegadas - Salidas")
plt.ylabel("")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "outputs/estaciones/top10_receptoras.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()




plt.figure(figsize=(10,6))

plt.barh(
    top10_emisoras["estacion"],
    abs(top10_emisoras["balance"])
)

plt.title("Estaciones con mayor balance negativo")
plt.xlabel("Salidas - Llegadas")
plt.ylabel("")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "outputs/estaciones/top10_emisoras.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


print("\nAnálisis de estaciones completado.")