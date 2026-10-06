import pandas as pd
from pathlib import Path


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    Base_DIR = Path(__file__).resolve().parent.parent
    archivo = Base_DIR / "data" / "data.csv.gz"

    data = pd.read_csv(
        archivo,
        compression="gzip",
        sep="\t",
        header=None
        )

    return list(data.groupby(0)[1].sum().sort_index().items())



if __name__ == "__main__":
    print(pregunta_03())


    
