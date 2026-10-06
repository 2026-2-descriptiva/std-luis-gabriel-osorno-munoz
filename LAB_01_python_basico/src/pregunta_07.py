import pandas as pd
from pathlib import Path


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, sep="\t", header = None, compression="gzip")


    resultados = data.groupby(1)[0].apply(list).reset_index().sort_values(1)

    resultados = resultados.apply(lambda x: (x[1], x[0]), axis=1).tolist()

    return resultados


if __name__ == "__main__":
    print(pregunta_07())
