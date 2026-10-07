import pandas as pd
from pathlib import Path


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl1.tsv"

    data = pd.read_csv(archivo, sep="\t")

    resultados = data["c4"].str.upper().unique()

    resultados = sorted(resultados)



    return resultados

if __name__ == "__main__":
    print(pregunta_06())



