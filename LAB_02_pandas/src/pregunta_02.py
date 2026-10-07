import pandas as pd
from pathlib import Path

def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl0.tsv"

    data = pd.read_csv(archivo, sep="\t", header=0)


    return data.shape[1]


if __name__ == "__main__":
    print(pregunta_02())

