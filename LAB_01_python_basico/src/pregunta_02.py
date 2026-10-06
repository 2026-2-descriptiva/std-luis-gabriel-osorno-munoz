# Cargado de las librerias

import pandas as pd
from pathlib import Path


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

        # Ruta del archivo data.csv.gz
    BASE_DIR = Path(__file__).resolve().parent.parent
    archivo = BASE_DIR / "data" / "data.csv.gz"

    # Leer el archivo
    data = pd.read_csv(
        archivo,
        compression="gzip",
        sep="\t",
        header=None
    )

    resultado = data[0].value_counts().sort_index()

    return list(resultado.items())


if __name__ == "__main__":
    pregunta_02()

