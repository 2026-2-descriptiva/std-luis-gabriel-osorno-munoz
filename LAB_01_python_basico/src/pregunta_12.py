import pandas as pd
from pathlib import Path


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, sep="\t", header=None, compression="gzip")


    data[5] = data[4].str.split(",")

    resultados = data[[0, 5]].explode(5)

    resultados[6] = resultados[5].str.split(":")

    resultados[6] = resultados[6].str[1].astype(int)

    resultados = resultados[[0,6]]

    resultados = resultados.groupby(0)[6].sum()

    resultados = resultados.to_dict()







    
    return resultados


if __name__ == "__main__":
    print(pregunta_12())
