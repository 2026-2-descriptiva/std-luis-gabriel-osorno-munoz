import pandas as pd
from pathlib import Path


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, compression="gzip", header = None, sep="\t")

    resultados = data.groupby(1)[0].apply(list)

    resultados = resultados.apply(lambda x: sorted(set(x))).reset_index().sort_values(1)

    resultados = resultados.apply(lambda x: (x[1], x[0]), axis=1).tolist()

    return resultados



if __name__ == "__main__":
    print(pregunta_08())
    
