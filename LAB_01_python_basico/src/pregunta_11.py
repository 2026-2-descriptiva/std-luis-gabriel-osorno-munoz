import pandas as pd
from pathlib import Path



def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "data.csv.gz"

    data = pd.read_csv(archivo, header = None, compression="gzip", sep="\t")

    resultados = data[[1, 3]]

    resultados[3] = resultados[3].str.split(",")

    resultados = resultados.explode(3)

    resultados = resultados.groupby(3)[1].sum().to_dict()

    return resultados



if __name__ == "__main__":
    print(pregunta_11())
