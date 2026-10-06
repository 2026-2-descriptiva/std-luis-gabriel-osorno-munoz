import pandas as pd
from pathlib import Path


def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, header=None, sep="\t", compression="gzip")

    resultados = data[[0, 3, 4]]

    resultados[3] = resultados[3].str.split(",").str.len()

    resultados[4] = resultados[4].str.split(",").str.len()

    resultados = list(zip(resultados[0], resultados[3], resultados[4]))

    return resultados

if __name__ == "__main__":
    print(pregunta_10())
    
