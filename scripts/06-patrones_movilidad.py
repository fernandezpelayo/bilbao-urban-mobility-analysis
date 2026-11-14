import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


Path("outputs/patrones_movilidad").mkdir(
    parents=True,
    exist_ok=True
)

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

df["fecha"] = pd.to_datetime(df["fecha"])


# -------------------
# VIAJES POR HORA
# -------------------

viajes_hora = df.groupby("hora").size()

plt.figure(figsize=(10,5))
viajes_hora.plot()
plt.title("Viajes por hora del día")
plt.xlabel("Hora")
plt.ylabel("Número de viajes")
plt.grid(True)
plt.tight_layout()
plt.savefig(
    "outputs/patrones_movilidad/viajes_por_hora.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()


# -------------------
# VIAJES POR DÍA SEMANA
# -------------------

dias = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

viajes_dia = (
    df.groupby("dia_semana")
      .size()
      .reindex(dias)
)

plt.figure(figsize=(8,5))
viajes_dia.plot(kind="bar")
plt.title("Viajes por día de la semana")
plt.xlabel("")
plt.ylabel("Número de viajes")
plt.tight_layout()
plt.savefig(
    "outputs/patrones_movilidad/viajes_por_dia_semana.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# -------------------
# VIAJES POR MES
# -------------------

viajes_mes = (
    df.groupby(
        df["fecha"].dt.month
    )
    .size()
)

plt.figure(figsize=(10,5))
viajes_mes.plot(marker="o")
plt.title("Viajes por mes")
plt.xlabel("Mes")
plt.ylabel("Número de viajes")
plt.grid(True)
plt.tight_layout()
plt.savefig(
    "outputs/patrones_movilidad/viajes_por_mes.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# -------------------
# VIAJES DIARIOS
# -------------------

viajes_diarios = (
    df.groupby("fecha")
      .size()
)

plt.figure(figsize=(14,5))
viajes_diarios.plot()
plt.title("Evolución diaria de viajes")
plt.xlabel("")
plt.ylabel("Número de viajes")
plt.tight_layout()
plt.savefig(
    "outputs/patrones_movilidad/viajes_diarios.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()