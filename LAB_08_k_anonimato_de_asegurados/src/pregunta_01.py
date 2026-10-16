import pandas as pd
from pathlib import Path
import json



################################################################################################
############################ Funciones de Anonimizacion ########################################
################################################################################################

def anonimous_age(series):

    edades = [17, 29, 39, 49, 65]

    labels = ["18-29", "30-39", "40-49", "50-64"]

    data = pd.cut(series, bins=edades, labels=labels, right=True)

    return data

def anonimous_bmi(series):

    pesos = [0, 18.5, 25, 30, 100]

    labels = ["bajo peso", "normal", "sobrepeso", "obesidad"]

    data = pd.cut(series, bins=pesos, labels=labels, right=False)

    return data

def anonimous_children(series):

    hijos = [-1, 0, 2, 100]

    labels = ["0", "1-2", "3+"]

    data = pd.cut(series, bins=hijos, labels = labels)

    return data


################################################################################################
######################################### Anonimizacion ########################################
################################################################################################

def anonimous(data):

    # Anonimizar la edad

    data = data.copy()

    data["age_group"] = anonimous_age(data["age"])

    # Anonimizar el bmi

    data["bmi_group"] = anonimous_bmi(data["bmi"])

    # Anonimizar los hijos

    data["children_group"] = anonimous_children(data["children"])

    return data


################################################################################################
######################################### Anonimizacion ########################################
################################################################################################











def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    # Lectura del dataset

    Base_dir = Path(__file__).parent.parent

    archivo = Base_dir / "data" / "insurance.csv.gz"

    data = pd.read_csv(archivo, compression="gzip")

    # Anonimización de la base de datos

    data_anonimus = anonimous(data)

    # Evaluación de los esquemas de generalización


    # Base de datos

    ## - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y `region`.

    columns_anonimus_with_children = ["age_group", "sex", "bmi_group", "children_group", "region"]


    data_with_children = data_anonimus[columns_anonimus_with_children]

    ## `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el número de hijos no se publica.

    columns_anonimus_without_children = ["age_group", "sex", "bmi_group", "region"]

    data_without_children = data_anonimus[columns_anonimus_without_children]

    # Verificacion de la privacidad

    ## Cuasiidentificadores originales

    ### original_k

    qi_original = ["age", "sex", "bmi", "children", "region"]

    original_k = int(data.groupby(qi_original).transform("size").min())

    ### original_unique_records

    original_unique_records = int(data.groupby(qi_original).transform("size").eq(1).sum().sum())


    # Definición de esquemas
    schemes_info = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"]
    }

    schemes_report = {}
    published_dfs = {}

    for scheme_name, qi_cols in schemes_info.items():
        # Agrupar por cuasi-identificadores del esquema
        class_sizes = data_anonimus.groupby(qi_cols, observed=False).transform("size")
        
        equivalence_classes = int(data_anonimus.groupby(qi_cols, observed=False).ngroups)
        k_before_suppression = int(class_sizes.min())

        # Suprimir registros con tamaño de clase < 5
        mask_published = class_sizes >= 5
        data_published = data_anonimus[mask_published].copy()

        suppressed_records = int((~mask_published).sum())
        published_records = int(mask_published.sum())

        # Clases de equivalencia publicadas
        published_classes = int(data_published.groupby(qi_cols, observed=False).ngroups)

        # Diversidad del atributo sensible ('smoker') en clases publicadas
        smoker_unique = data_published.groupby(qi_cols, observed=False)["smoker"].transform("nunique")
        
        # Una clase carece de diversidad si tiene un solo valor único de smoker
        no_diversity_mask = smoker_unique == 1
        records_without_smoker_diversity = int(no_diversity_mask.sum())
        
        # Conteo de clases sin diversidad
        if published_records > 0:
            classes_no_div = data_published[no_diversity_mask].groupby(qi_cols, observed=False).ngroups
        else:
            classes_no_div = 0
        
        classes_without_smoker_diversity = int(classes_no_div)

        schemes_report[scheme_name] = {
            "quasi_identifiers": qi_cols,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_without_smoker_diversity,
            "records_without_smoker_diversity": records_without_smoker_diversity
        }

        published_dfs[scheme_name] = data_published

    # 3. Seleccionar esquema con menor registros suprimidos
    selected_scheme = min(
        schemes_report.keys(),
        key=lambda s: schemes_report[s]["suppressed_records"]
    )

    df_selected = published_dfs[selected_scheme]

    # Promedios y tasas de fumadores
    mean_charges_original = float(data["charges"].mean())
    mean_charges_published = float(df_selected["charges"].mean())

    smoker_rate_original = float((data["smoker"] == "yes").mean())
    smoker_rate_published = float((df_selected["smoker"] == "yes").mean())

    # Crear reporte final
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes_report,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published
    }

    # 4. Guardar archivos requeridos
    submission_dir = Base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    # Escribir json
    with open(submission_dir / "privacy_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # Escribir CSV publicado con el orden original
    published_cols = schemes_info[selected_scheme] + ["smoker", "charges"]
    df_selected[published_cols].to_csv(
        submission_dir / "insurance_published.csv",
        index=False
    )



    return report




















    return schemes_inf



if __name__ == "__main__":
    print(pregunta_01())
