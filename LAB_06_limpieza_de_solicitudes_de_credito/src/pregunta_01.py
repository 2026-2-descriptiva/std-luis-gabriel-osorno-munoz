import pandas as pd
import numpy as np
from pathlib import Path
import re

######### Step 1 #########

# -------------------------------------------------

def columns_selector(data):

    columns_names = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
                            "estrato", "comuna_ciudadano", "fecha_de_beneficio", 
                            "monto_del_credito", "línea_credito"]

    data_output = data[columns_names]

    return data_output

######### Step 2 #########

def clean_column_sexo(series):

    data = series.str.lower().str.strip()

    return data

def clean_column_tipo_de_emprendimiento(series):

    data = series.str.strip().str.lower()

    return data

def clean_column_idea_negocio(series):

    data = series.str.lower().str.replace("-", " ").str.rstrip()

    return data

def clean_column_barrio(series):

    data = series.str.lower().str.replace("-", " ").str.rstrip()

    return data

def clean_column_linea_credito(series):

    data = series.str.lower().str.replace("-", " ").str.rstrip()

    return data

def clean_columns_text(data):

    # Cleaning of sexo

    data.loc[:, "sexo"] = clean_column_sexo(data["sexo"])

    # Cleaning of tipo_de_emprendimiento

    data.loc[:,"tipo_de_emprendimiento"] = clean_column_tipo_de_emprendimiento(data["tipo_de_emprendimiento"])

    # Cleaning of idea_negocio

    data.loc[:, "idea_negocio"] = clean_column_idea_negocio(data["idea_negocio"])

    # Cleaning of barrio

    data.loc[:, "barrio"] = clean_column_barrio(data["barrio"])

    # Cleaning of línea_credito

    data.loc[:, "línea_credito"] = clean_column_linea_credito(data["línea_credito"])

    return data

######### Step 3 #########

def clean_column_estrato(series):

    data = series.astype(int)

    return data

def clean_column_monto_del_credito(series):

    data = (series.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".00", "", regex=False)
            .str.strip()
            .astype(float)
            .astype(int))

    return data

def clean_column_comuna_ciudadano(series):

    data = pd.to_numeric(series, errors="coerce").astype("Int64")

    return data

def clean_columns_numeric(data):  

    # Cleaning of estrato

    data.loc[:, "estrato"]  = clean_column_estrato(data["estrato"])

    # Cleaning of monto_del_credito

    data.loc[:, "monto_del_credito"] = clean_column_monto_del_credito(data["monto_del_credito"])

    # Cleaning of comuna_ciudadano

    data["comuna_ciudadano"] = pd.to_numeric(data["comuna_ciudadano"], errors="coerce").astype("Int64")

    return data

######### Step 4 #########

def sort_fecha(series):
    def change_date(fecha):
        lista = fecha.split("-")
        if len(lista) != 3:
            return fecha

        p1, p2, p3 = lista

        try:
            # Caso 1: El año de 4 dígitos está al inicio (YYYY-MM-DD o YYYY-DD-MM)
            if len(p1) == 4:
                year = p1
                val1, val2 = int(p2), int(p3)
                
                # Si val1 > 12, sabemos que p2 es el día (YYYY-DD-MM)
                if val1 > 12:
                    day, month = val1, val2
                else:
                    month, day = val1, val2
                return f"{year}-{month:02d}-{day:02d}"

            # Caso 2: El año de 4 dígitos está al final (DD-MM-YYYY o MM-DD-YYYY)
            elif len(p3) == 4:
                year = p3
                val1, val2 = int(p1), int(p2)
                
                # Si val2 > 12, p2 es el día (MM-DD-YYYY)
                if val2 > 12:
                    month, day = val1, val2
                # Si val1 > 12 o formato estándar DD-MM-YYYY
                else:
                    day, month = val1, val2
                    
                return f"{year}-{month:02d}-{day:02d}"

            return fecha
        except (ValueError, TypeError):
            return fecha

    return series.apply(change_date)

def clean_column_date(data):
    series = data["fecha_de_beneficio"].astype(str).str.strip()

    # 1. Convertir todas las "/" a "-"
    series = series.str.replace("/", "-", regex=False)

    # 2. Reorganizar y estandarizar a YYYY-MM-DD con sort_fecha
    series = sort_fecha(series)

    data.loc[:, "fecha_de_beneficio"] = series
    return data

######### Step 5 #########

def remove_missing_except_comuna_ciudadano(data):

    col_no_drop_na = ["comuna_ciudadano"]

    col_to_drop_na = data.columns.difference(col_no_drop_na)

    data_clean = data.dropna(subset=col_to_drop_na)

    return data_clean

######### Step 6 #########

def remove_duplicated(data):

    output_data = data.drop_duplicates()

    return output_data






def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    Base_file = Path(__file__).parent.parent

    file = Base_file / "data" / "solicitudes_de_credito.csv.gz"

    # Read of dataset

    data = pd.read_csv(file, compression="gzip", sep=";")
    
    # Step 1: Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`, 
    # `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
    # `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese orden.

    data_filter = data.copy()

    data_filter = columns_selector(data=data_filter)
    
    # Step 2: Los campos de texto están en minúsculas y sus palabras separadas por espacios.

    data_filter = clean_columns_text(data_filter)

    # Step 3: `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
    # separadores de miles.

    data_filter = clean_columns_numeric(data_filter)

    # Step 4: Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por 
    # ejemplo `AAAA-MM-DD`

    data_filter = clean_column_date(data_filter)

    # Step 5: No hay registros incompletos. La única excepción es 
    # `comuna_ciudadano`: sus valores faltantes son parte de los datos
    # originales y deben conservarse.

    data_filter = remove_missing_except_comuna_ciudadano(data_filter)

    # Step 6: No hay registros duplicados.

    data_filter = remove_duplicated(data_filter)

    # Guardado de los datos

    File_output = Base_file / "submission" / "solicitudes_de_credito.csv"

    data_filter.to_csv(File_output, sep=";", index = False)

    # Verificación de que el proceso quedó correcto

    resultados = len(data_filter["fecha_de_beneficio"])

    return resultados


if __name__ == "__main__":
    print(pregunta_01())
