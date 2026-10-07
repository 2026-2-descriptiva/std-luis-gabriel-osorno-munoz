import pandas as pd
from pathlib import Path
import re

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "clusters_report.txt"

    registros = []

    cluster_actual = None

    with open(archivo, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    for linea in lineas[4:]:
        linea_str = linea.strip()
        
        # Saltar líneas vacías
        if not linea_str:
            continue

        # Detectar si la línea empieza con datos de un nuevo cluster (un número al inicio)
        # Regex captura: 1. cluster, 2. cantidad, 3. porcentaje, 4. inicio de palabras clave
        match = re.match(r"^(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$", linea_str)

        if match:
            # Si ya teníamos acumulado un cluster previo, lo guardamos en la lista
            if cluster_actual:
                registros.append(cluster_actual)

            # Extraer las 4 partes
            cluster, cantidad, porcentaje, palabras = match.groups()

            # Guardar el nuevo cluster en un diccionario
            cluster_actual = {
                "cluster": int(cluster),
                "cantidad_de_palabras_clave": int(cantidad),
                "porcentaje_de_palabras_clave": float(porcentaje.replace(",", ".")),
                "principales_palabras_clave": palabras.strip()
            }
        else:
            # Si no empieza con número, es una línea de continuación de palabras clave
            if cluster_actual:
                cluster_actual["principales_palabras_clave"] += " " + linea.strip()

    if cluster_actual:
        registros.append(cluster_actual)

    # 4. Crear el DataFrame inicial a partir de los registros procesados
    df = pd.DataFrame(registros)

    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.rstrip(".")
    )
    
    return df


if __name__ == "__main__":
    print(pregunta_01())
