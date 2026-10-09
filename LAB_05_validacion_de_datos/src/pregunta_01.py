import pandas as pd
from pathlib import Path
import re
import json
import numpy as np


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    # Cargado de la base de datos

    Base_file = Path(__file__).parent.parent

    file = Base_file / "data" / "ventas.csv.gz"

    data = pd.read_csv(file, compression="gzip")

    # Limpieza de los nombres de las columnas

    nombres_columns = data.columns

    nombres_columns = nombres_columns.str.lower().str.strip().str.replace(" ", "_")

    data.columns = nombres_columns

    # Pregunta 1: `row_count`: cantidad de filas de datos.

    row_count = data.shape[0]

    # Pregunta 2: `column_count`: cantidad de columnas.

    column_count = data.shape[1]

    # Pregunta 3: `missing_required_columns`: lista ordenada de columnas requeridas que no están en el archivo.

    columnas_requeridas = ["supplier_id", "supplier", "country", "city",
                            "purchase_date", "amount", "discount", "weight",
                            "units", "unit_price", "contact_email"]

    columnas_leidas = data.columns

    missing_required_columns = list(set(columnas_leidas) - set(columnas_requeridas))

    # Pregunta 4 `unexpected_columns`: lista ordenada de columnas del archivo que no son requeridas.

    unexpected_columns = list(set(columnas_leidas)-set(columnas_requeridas))

    # Pregunta 5 `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.

    filas_unicas = data.drop_duplicates()

    duplicate_row_count = data.shape[0] - filas_unicas.shape[0]

    # Pregunta 6 `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
    # aparece más de una vez (cuente todas esas filas, no solo las
    # repetidas).

    duplicate_supplier_id_row_count = int(data["supplier_id"].duplicated(keep=False).sum())

    # Pregunta 7 `missing_value_count_by_column`: diccionario con la cantidad de valores 
    # faltantes de cada columna. Considere faltantes las celdas vacías y las
    # que contienen `N/A`.
  
    missing_value_count_by_column = dict(data.isna().sum())

    # Pregunta 8 `invalid_email_count`: cantidad de valores de `contact_email` que no 
    # tienen la forma `usuario@dominio.extension`.

    invalid_email_count = sum(~data["contact_email"].str.contains(pat="@", regex=True))

    # Pregunta 9 `invalid_unit_count`: cantidad de valores numéricos de `units` que no son 
    # enteros positivos. Los valores faltantes no se cuentan aquí

    invalid_unit_count = int((data["units"] <= 0).sum())


    # Pregunta 10 `country_values`: lista ordenada de los valores distintos de `country`, 
    # escritos exactamente como aparecen en el archivo.

    country = len(sorted(data["country"].dropna().unique().tolist()))

    country_values = sorted(data["country"].dropna().unique().tolist())


    summary = {"row_count" : row_count, "column_count":column_count, 
               "missing_required_columns":missing_required_columns, "unexpected_columns" : unexpected_columns,
               "duplicate_row_count":duplicate_row_count, "duplicate_supplier_id_row_count" : duplicate_supplier_id_row_count,
               "missing_value_count_by_column" : missing_value_count_by_column, "invalid_email_count":invalid_email_count,
               "invalid_unit_count":invalid_unit_count, "country" :country,
               "country_values" : country_values}

    def convert_numpy(obj):
      if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
      elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
      elif isinstance(obj, np.ndarray):
        return obj.tolist()
      raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    # Guardar los resultados 

    ruta_save = Base_file / "submission" / "data_quality_report.json"

    ruta_save.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_save, "w", encoding="utf-8") as f:
      json.dump(summary, f, indent=4, default=convert_numpy)

    return summary


if __name__ == "__main__":
    print(main())
