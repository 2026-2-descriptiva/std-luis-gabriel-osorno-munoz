import pandas as pd
from pathlib import Path




def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    Base_Dir = Path(__file__).resolve().parent.parent

    archivo = Base_Dir / "data" / "data.csv.gz"


    data = pd.read_csv(archivo, compression="gzip", sep="\t", header=None)

    fecha = data[2].str.split("-")

    fechas = dict()

    for i in fecha:

        if i[1] in fechas:
            fechas[i[1]] += 1
        else:
            fechas[i[1]] = 1


    return sorted(fechas.items(), key=lambda x: x[0])

if __name__ == "__main__":
    print(pregunta_04())