import pandas as pd
from pathlib import Path

def pregunta_08():
    """
    Retorne la tabla `data/tbl0.tsv` completa con una columna adicional
    llamada `suma`, al final, cuyo valor en cada fila es `c0 + c2`.

    Ejemplo del formato de la respuesta:

            c0 c1  c2          c3  suma
        0    0  E   1  1999-02-28     1
        1    1  A   2  1999-10-28     3
        2    2  B   5  1998-05-02     7
        ...
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "tbl0.tsv"

    data = pd.read_csv(archivo, sep = "\t")

    data["suma"] = data["c0"]+data["c2"]

    return data


if __name__ == "__main__":
    print(pregunta_08())
