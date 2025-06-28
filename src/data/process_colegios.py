import pandas as pd
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta al archivo de entrada
input_path = os.path.join(BASE_DIR, "data", "raw", "colegios.csv")

output_path = os.path.join(BASE_DIR, "data", "processed", "colegios_processed.csv")

df_raw = pd.read_csv(input_path, sep="|")

df = df_raw.copy()

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("/", "_")
    .str.replace("__", "_")
    .str.replace("á", "a").str.replace("é", "e")
    .str.replace("í", "i").str.replace("ó", "o").str.replace("ú", "u")
)

columns_to_drop = ["codigo_modular", "anexo", "ubigeo", "codigo_dre_ugel", "dre___ugel", "centro_poblado", "codigo_centro_poblado", "codigo_local", "altitud", "fuente_de_coordenadas"]

df = df.drop(columns=columns_to_drop, errors="ignore")

for col in df.select_dtypes(include="object").columns:
    df[col] = (
        df[col] 
        .astype(str)
        .str.strip()
        .str.lower()
        .str.normalize("NFKD")  # quitar tildes y acentos
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
    )

df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")

df.to_csv(output_path, index=False)
