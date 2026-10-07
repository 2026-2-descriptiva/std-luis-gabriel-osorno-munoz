import pandas as pd
from pathlib import Path


def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl0.tsv"

    data = pd.read_csv(archivo, sep="\t", header=0)

    resultados = data["c1"].value_counts().sort_index()

    return resultados


if __name__ == "__main__":
    print(pregunta_03())

