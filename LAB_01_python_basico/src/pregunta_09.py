import pandas as pd
from pathlib import Path


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, header= None, sep="\t", compression="gzip")

    resultados = data[4]

    resultados = resultados.str.split(",")

    for i in range(len(resultados)):
        resultados[i] = [x.split(":")[0] for x in resultados[i]]

    resultados = resultados.explode().value_counts().sort_index().to_dict()

    return resultados 


if __name__ =="__main__":
    print(pregunta_09())
