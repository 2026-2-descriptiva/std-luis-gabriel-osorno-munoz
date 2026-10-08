import pandas as pd
import os
from pathlib import Path
import glob

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    # Obtener el directorio de trabajo

    Base_dir = Path(__file__).parent.parent

    # Recorrer los archivos de train

    rutas_train = Base_dir / "data" / "train"

    ## Se obtienen las emociones

    emotions_train = sorted([archivo for archivo in os.listdir(rutas_train)])


    # Se crea el diccionario para almacenar

    lista_emotions_train = []

    # Se inicia el for

    for emo in emotions_train:

        archivo_dir = rutas_train / emo

        archivos = sorted([f for f in archivo_dir.glob("*") if f.is_file()], key=lambda f: f.name)

        for archivo in archivos:

            texto = archivo.read_text(encoding="utf-8").strip()

            lista_emotions_train.append({"phrase": texto,
                                         "target":emo})

    # Se convierte en un dataframe

    dataframe_train = pd.DataFrame(lista_emotions_train)

    # Se guarda el dataset en submission/train_dataset.csv

    carpeta_save_train = Base_dir / "submission" / "train_dataset.csv"

    dataframe_train.to_csv(carpeta_save_train, index=False, encoding="utf-8")

    # Recorrer los archivos de test

    rutas_test = Base_dir / "data" / "test"

    # Definimos las emociones en test

    emociones_test = sorted([archivo for archivo in os.listdir(rutas_test)])

    lista_emotions_test = []

    for emo in emociones_test:

        archivo_test = rutas_test / emo

        archivos = sorted([f for f in archivo_test.glob("*") if f.is_file()], key=lambda f: f.name)

        for file in archivos:

            texto = file.read_text(encoding="utf-8").strip()

            lista_emotions_test.append({"phrase" : texto,
                                        "target" : emo})

    dataframe_test = pd.DataFrame(lista_emotions_test)

    carpeta_save_test = Base_dir / "submission" / "test_dataset.csv"

    dataframe_test.to_csv(carpeta_save_test, index=False, encoding="utf-8")

    return "Hecho"



if __name__ == "__main__":
    print(pregunta_01())
