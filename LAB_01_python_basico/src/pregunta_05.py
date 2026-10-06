import pandas as pd
from pathlib import Path

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    Base_dir = Path(__file__).resolve().parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, compression="gzip", sep="\t", header=None)

    resultado = data.groupby(0)[1].agg(['max', 'min']).reset_index()

    return resultado.sort_values(0).apply(lambda x: (x[0], x['max'], x['min']), axis=1).tolist()



if __name__ == "__main__":
    print(pregunta_05())
