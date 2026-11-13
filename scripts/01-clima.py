import os
import time
import calendar
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AEMET_API_KEY")

if not api_key:
    raise ValueError(
        "No se ha encontrado AEMET_API_KEY. "
        "Configura tu clave de AEMET en el archivo .env."
    )

BASE_URL = (
    "https://opendata.aemet.es/opendata/api/"
    "valores/climatologicos/diarios/datos"
)

def get_month_data(month):

    year = 2021

    last_day = calendar.monthrange(year, month)[1]

    start = f"{year}-{month:02d}-01T00:00:00UTC"
    end = f"{year}-{month:02d}-{last_day}T23:59:59UTC"

    url = f"{BASE_URL}/fechaini/{start}/fechafin/{end}/estacion/1082"

    for attempt in range(5):

        try:

            r = requests.get(
                url,
                params={"api_key": api_key},
                timeout=30
            )

            data = r.json()

            if "datos" not in data:

                print(f"Error mes {month}")
                print(data)

                time.sleep(30)

                continue

            data_url = data["datos"]

            time.sleep(5)

            
            r2 = requests.get(data_url, timeout=30)

            if r2.status_code != 200:
                print(f"Error descargando datos del mes {month}")
                continue

            return pd.DataFrame(r2.json())

        except Exception as e:

            print(e)

            time.sleep(30)

    return None

all_data = []
failed_months = []

for month in range(1, 13):

    print(f"Mes {month}")

    df = get_month_data(month)

    if df is not None and not df.empty:
        all_data.append(df)
    else:
        failed_months.append(month)

    time.sleep(10)
    
if failed_months:
    raise ValueError(
        f"No se han podido descargar los siguientes meses: {failed_months}. "
        "Vuelve a ejecutar el script para completar la descarga."
    )

if not all_data:
    raise ValueError("No se ha descargado ningún dato de AEMET.")

final = pd.concat(
    all_data,
    ignore_index=True
)

final.to_csv(
    "data/raw/clima_2021.csv",
    index=False
)

print(final.shape)

print(final["fecha"].min())
print(final["fecha"].max())
print(len(final))
print(
    pd.to_datetime(final["fecha"])
    .dt.to_period("M")
    .value_counts()
    .sort_index()
)
