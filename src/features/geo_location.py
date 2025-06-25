#%%
import pandas as pd
import googlemaps
from time import sleep

def obtener_coordenadas(direccion, contador=None):
    try:
        resultado = gmaps.geocode(direccion)
        if resultado:
            latitud = resultado[0]["geometry"]["location"]["lat"]
            longitud = resultado[0]["geometry"]["location"]["lng"]
            print(f"[{contador}] ✅ Coordenadas encontradas para: {direccion}")
            return latitud, longitud
        else:
            print(f"[{contador}] ⚠️ No se encontraron coordenadas para: {direccion}")
            return None, None
    except Exception as e:
        print(f"[{contador}] ❌ Error al geocodificar '{direccion}': {e}")
        return None, None



input_path =  "D:/DS_Portafolio/casas/data/processed/adondevivir_processed_geo.csv"

df = pd.read_csv(input_path)

API_KEY = "AIzaSyAJRfznV_Rqcw04dpKWv8qUvJs3GTWbp-s"  # Tu clave aquí
gmaps = googlemaps.Client(key=API_KEY)

df["direccion_completa"] = df["direccion_limpia"] + ", " + df["distrito"]

# Aplicar geocodificación con contador
latitudes = []
longitudes = []

for i, row in enumerate(df.itertuples(), start=1):
    direccion = row.direccion_completa
    lat, lon = obtener_coordenadas(direccion, contador=i)
    latitudes.append(lat)
    longitudes.append(lon)
    sleep(1)

# Asignar al DataFrame
df["latitud"] = latitudes
df["longitud"] = longitudes

df.to_csv("D:/DS_Portafolio/casas/data/processed/adondevivir_processed_geo.csv")
