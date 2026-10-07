import pandas as pd
from pathlib import Path

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo1 = Base_dir / "data" / "tbl0.tsv"

    archivo2 = Base_dir / "data" / "tbl2.tsv"

    data1 = pd.read_csv(archivo1, sep="\t")

    data2 = pd.read_csv(archivo2, sep="\t")

    data = pd.merge(data1, data2, on="c0")

    resultados = data.groupby("c1")["c5b"].sum()



    return resultados


if __name__ == "__main__":

    print(pregunta_13())
