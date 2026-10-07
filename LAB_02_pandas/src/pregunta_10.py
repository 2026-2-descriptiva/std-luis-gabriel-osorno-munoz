import pandas as pd
from pathlib import Path

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl0.tsv"

    data = pd.read_csv(archivo, sep="\t")

    resultados = data.copy()

    resultados = resultados.groupby("c1")["c2"].agg(c2=lambda x: ":".join(map(str, sorted(x))))

    return resultados

if __name__ == "__main__":
    print(pregunta_10())


