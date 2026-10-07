import pandas as pd
from pathlib import Path

def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl0.tsv"

    data = pd.read_csv(archivo, sep="\t")

    resultados = data.groupby("c1")["c2"].sum()

    return resultados


if __name__ ==  "__main__":
    print(pregunta_07())


