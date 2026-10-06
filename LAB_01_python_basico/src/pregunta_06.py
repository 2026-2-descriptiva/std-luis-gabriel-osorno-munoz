import pandas as pd
from pathlib import Path


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    Base_dir = Path(__file__).resolve().parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, header=None, compression="gzip", sep="\t")

    resultados = data[4].str.split(",")

    resultados = resultados.apply(lambda x: [i.split(":") for i in x]) 

    resultados = resultados.explode().apply(lambda x: pd.Series(x, index=["clave", "valor"]))

    resultados["valor"] = resultados["valor"].astype(int)

    resultados = resultados.groupby("clave")["valor"].agg(["min", "max"]).reset_index()

    resultados = resultados.sort_values("clave").apply(lambda x: (x["clave"], x["min"], x["max"]), axis=1).tolist()

    return resultados

if __name__ == "__main__":
    print(pregunta_06())