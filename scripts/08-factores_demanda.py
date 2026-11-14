import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("outputs/factores_demanda").mkdir(
    parents=True,
    exist_ok=True
)

# =========================
# CARGA DE DATOS
# =========================

df = pd.read_csv(
    "data/processed/df_final_limpio.csv.gz",
    compression="gzip",
    low_memory=False
)

df["fecha"] = pd.to_datetime(df["fecha"])


# =========================
# CONSTRUCCIÓN DEMANDA DIARIA
# =========================

demanda = (
    df.groupby("fecha")
    .agg({
        "uid": "count",
        "tmin": "first",
        "tmed": "first",
        "tmax": "first",
        "prec": "first",
        "sol": "first",
        "velmedia": "first"
    })
    .rename(
        columns={
            "uid": "viajes"
        }
    )
)


# ==================================================
# CALENDARIO
# ==================================================


# =========================
# DÍA DE LA SEMANA
# =========================

demanda["dia_semana"] = demanda.index.day_name()

dias = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

media_dia = (
    demanda
    .groupby("dia_semana")["viajes"]
    .mean()
    .reindex(dias)
)


print("\n" + "="*50)
print("MEDIA POR DÍA DE LA SEMANA")
print("="*50)

print(media_dia)


plt.figure(figsize=(10, 5))

media_dia.plot(
    kind="bar"
)

plt.title(
    "Demanda media por día de la semana"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()

plt.savefig(
    "outputs/factores_demanda/viajes_dia_semana.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =========================
# TIPO DE DÍA
# =========================


festivos = [
    "2021-01-01",
    "2021-01-06",
    "2021-03-19",
    "2021-04-01",
    "2021-04-02",
    "2021-04-05",
    "2021-05-01",
    "2021-07-31",
    "2021-08-27",
    "2021-10-12",
    "2021-11-01",
    "2021-12-06",
    "2021-12-08",
    "2021-12-25"
]

festivos = pd.to_datetime(festivos)


demanda["tipo_dia"] = "Laborable"

demanda.loc[
    demanda.index.day_of_week >= 5,
    "tipo_dia"
] = "Fin de semana"


demanda.loc[
    demanda.index.isin(festivos),
    "tipo_dia"
] = "Festivo"


media_tipo = (
    demanda
    .groupby("tipo_dia")["viajes"]
    .mean()
    .reindex(
        [
            "Laborable",
            "Fin de semana",
            "Festivo"
        ]
    )
)


print("\n" + "="*50)
print("MEDIA POR TIPO DE DÍA")
print("="*50)

print(media_tipo)


plt.figure(figsize=(8, 5))

media_tipo.plot(
    kind="bar"
)

plt.title(
    "Demanda media según tipo de día"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()


plt.savefig(
    "outputs/factores_demanda/viajes_tipo_dia.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()



# =========================
# ESTACIONALIDAD MENSUAL
# =========================


demanda["mes"] = demanda.index.month


media_mes = (
    demanda
    .groupby("mes")["viajes"]
    .mean()
)


print("\n" + "="*50)
print("DEMANDA MEDIA POR MES")
print("="*50)

print(media_mes)


plt.figure(figsize=(10, 5))

media_mes.plot(
    marker="o"
)

plt.title(
    "Demanda media mensual"
)

plt.xlabel("Mes")
plt.ylabel("Viajes medios")

plt.grid(True)

plt.tight_layout()


plt.savefig(
    "outputs/factores_demanda/viajes_mes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =========================
# DÍAS ANÓMALOS
# =========================


print("\n" + "="*50)
print("DÍAS CON MENOR DEMANDA")
print("="*50)


print(
    demanda
    .sort_values("viajes")
    .head(30)
)

# ==================================================
# CLIMA
# ==================================================


# =========================
# CORRELACIONES CLIMÁTICAS
# =========================


correlaciones = demanda[
    [
        "viajes",
        "tmin",
        "tmed",
        "tmax",
        "prec",
        "sol",
        "velmedia"
    ]
].corr()


print("\n" + "="*50)
print("CORRELACIONES CLIMÁTICAS")
print("="*50)

print(
    correlaciones["viajes"]
    .sort_values(ascending=False)
)

# =========================
# LLUVIA POR RANGOS
# =========================


rangos_lluvia = [
    -1,
    0,
    5,
    20,
    demanda["prec"].max()
]


etiquetas = [
    "0 mm",
    "0-5 mm",
    "5-20 mm",
    ">20 mm"
]


demanda["lluvia_rango"] = pd.cut(
    demanda["prec"],
    bins=rangos_lluvia,
    labels=etiquetas
)


lluvia_media = (
    demanda
    .groupby("lluvia_rango")["viajes"]
    .mean()
)


print("\n" + "="*50)
print("DEMANDA SEGÚN LLUVIA")
print("="*50)

print(lluvia_media)


plt.figure(figsize=(8, 5))

lluvia_media.plot(
    kind="bar"
)

plt.title(
    "Demanda media según precipitación"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()


plt.savefig(
    "outputs/factores_demanda/viajes_lluvia.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("\n" + "="*50)
print("NÚMERO DE DÍAS POR RANGO DE LLUVIA")
print("="*50)

print(
    demanda["lluvia_rango"]
    .value_counts()
    .sort_index()
)

# =========================
# DEMANDA SEGÚN HORAS DE SOL
# =========================


demanda["sol_rango"] = pd.cut(
    demanda["sol"],
    bins=[
        -0.1,
        0,
        4,
        8,
        24
    ],
    labels=[
        "0 h",
        "0-4 h",
        "4-8 h",
        ">8 h"
    ]
)


sol_media = (
    demanda
    .groupby("sol_rango")["viajes"]
    .mean()
)


print("\n" + "="*50)
print("DEMANDA SEGÚN HORAS DE SOL")
print("="*50)

print(sol_media)


plt.figure(figsize=(8,5))

sol_media.plot(
    kind="bar"
)

plt.title(
    "Demanda media según horas de sol"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()


plt.savefig(
    "outputs/factores_demanda/viajes_sol.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("\n" + "="*50)
print("NÚMERO DE DÍAS POR RANGO DE SOL")
print("="*50)

print(
    demanda["sol_rango"]
    .value_counts()
    .sort_index()
)

# ===================================
# DEMANDA SEGÚN TEMPERATURA MÁXIMA
# ===================================

demanda["tmax_rango"] = pd.cut(
    demanda["tmax"],
    bins=[
        -10,
        10,
        15,
        20,
        25,
        30,
        50
    ],
    labels=[
        "<10ºC",
        "10-15ºC",
        "15-20ºC",
        "20-25ºC",
        "25-30ºC",
        ">30ºC"
    ]
)


temp_media = (
    demanda
    .groupby("tmax_rango")["viajes"]
    .mean()
)


print("\n" + "="*50)
print("DEMANDA SEGÚN TEMPERATURA MÁXIMA")
print("="*50)

print(temp_media)


plt.figure(figsize=(8,5))

temp_media.plot(
    kind="bar"
)

plt.title(
    "Demanda media según temperatura máxima"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()


plt.savefig(
    "outputs/factores_demanda/viajes_temperatura_maxima.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("\n" + "="*50)
print("NÚMERO DE DÍAS POR RANGO DE TEMPERATURA")
print("="*50)

print(
    demanda["tmax_rango"]
    .value_counts()
    .sort_index()
)


# ==================================================
# CLIMA EN DÍAS LABORABLES
# ==================================================

laborables = demanda[
    demanda["tipo_dia"] == "Laborable"
].copy()


# =========================
# LLUVIA EN DÍAS LABORABLES
# =========================


laborables["lluvia_rango"] = pd.cut(
    laborables["prec"],
   bins=[-1,0,5,20,laborables["prec"].max()],
    labels=[
        "0 mm",
        "0-5 mm",
        "5-20 mm",
        ">20 mm"
    ]
)


lluvia_lab_media = (
    laborables
    .groupby("lluvia_rango")["viajes"]
    .mean()
)

print("\n" + "="*50)
print("LABORABLES: DEMANDA SEGÚN LLUVIA")
print("="*50)


print(lluvia_lab_media)


print("\n" + "="*50)
print("LABORABLES: NÚMERO DE DÍAS POR LLUVIA")
print("="*50)


print(
    laborables["lluvia_rango"]
    .value_counts()
    .sort_index()
)


plt.figure(figsize=(8,5))

lluvia_lab_media.plot(
    kind="bar"
)

plt.title(
    "Laborables: demanda según lluvia"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()

plt.savefig(
    "outputs/factores_demanda/demanda_lluvia_laborables.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =========================
# SOL EN DÍAS LABORABLES
# =========================


laborables["sol_rango"] = pd.cut(
    laborables["sol"],
    bins=[-0.1,0,4,8,24],
    labels=[
        "0 h",
        "0-4 h",
        "4-8 h",
        ">8 h"
    ]
)


sol_lab_media = (
    laborables
    .groupby("sol_rango")["viajes"]
    .mean()
)


print("\n" + "="*50)
print("LABORABLES: DEMANDA SEGÚN SOL")
print("="*50)


print(sol_lab_media)


print("\n" + "="*50)
print("LABORABLES: NÚMERO DE DÍAS POR SOL")
print("="*50)


print(
    laborables["sol_rango"]
    .value_counts()
    .sort_index()
)


plt.figure(figsize=(8,5))

sol_lab_media.plot(
    kind="bar"
)

plt.title(
    "Laborables: demanda según horas de sol"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()

plt.savefig(
    "outputs/factores_demanda/demanda_sol_laborables.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ===================================
# TEMPERATURA MÁXIMA EN DÍAS LABORABLES
# ===================================


laborables["tmax_rango"] = pd.cut(
    laborables["tmax"],
    bins=[-10, 10, 15, 20, 25, 30, 50],
    labels=[
        "<10ºC",
        "10-15ºC",
        "15-20ºC",
        "20-25ºC",
        "25-30ºC",
        ">30ºC"
    ]
)


tmax_lab_media = (
    laborables
    .groupby("tmax_rango")["viajes"]
    .mean()
)

print("\n" + "="*50)
print("LABORABLES: DEMANDA SEGÚN TEMPERATURA MÁXIMA")
print("="*50)

print(tmax_lab_media)



print("\n" + "="*50)
print("LABORABLES: NÚMERO DE DÍAS POR TEMPERATURA")
print("="*50)


print(
    laborables["tmax_rango"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8,5))


tmax_lab_media.plot(
    kind="bar"
)

plt.title(
    "Laborables: demanda según temperatura máxima"
)

plt.xlabel("")
plt.ylabel("Viajes medios")

plt.tight_layout()

plt.savefig(
    "outputs/factores_demanda/demanda_tmax_laborables.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()