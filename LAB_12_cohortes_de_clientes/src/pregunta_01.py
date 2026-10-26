import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
      `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
      `retention_rate`, y una fila por cada combinación cohorte–período
      observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
      con una fila por cohorte (eje vertical) y una columna por período
      (eje horizontal). Muestre los valores como porcentajes. Los períodos
      que todavía no se pueden observar para una cohorte no significan
      retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    #####################################################################################
    ############################# Lectura de la base de datos ###########################
    #####################################################################################
    

    base_dir = Path(__file__).parent.parent

    file = base_dir / "data" / "sales.csv.gz"

    data = pd.read_csv(file, compression="gzip")


    #####################################################################################
    ############################# Operaciones sobre el dataset ##########################
    #####################################################################################

    # - `cohort_month`: el mes de la primera compra del cliente, escrito como
    #  `AAAA-MM`

    data["OrderDate"] = pd.to_datetime(data["OrderDate"])

    data["cohort_month"] = data.groupby("CustomerID")["OrderDate"].transform("min")
    
    data["cohort_month"] = data["cohort_month"].dt.strftime("%Y-%m")

    # - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
    #      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.

    data["cohort_month"] = pd.to_datetime(data["cohort_month"])

    data["cohort_year"] = data["cohort_month"].dt.strftime("%Y").astype(int)
    data["cohort_mes"] = data["cohort_month"].dt.strftime("%m").astype(int)

    data["cohort_year_now"] = data["OrderDate"].dt.strftime("%Y").astype(int)
    data["cohort_mes_now"] = data["OrderDate"].dt.strftime("%m").astype(int)

    data["period_index"] = (data["cohort_year_now"]-data["cohort_year"])*12 + (data["cohort_mes_now"]-data["cohort_mes"])

    data["cohort_month"] = data["cohort_month"].dt.strftime("%Y-%m")

    # - `active_customers`: la cantidad de clientes distintos de la cohorte que
    #      compraron en ese período.

    cohort_data = data.groupby(["cohort_month", "period_index"], as_index = False).agg(
        active_customers=("CustomerID", "nunique")
        )

    # - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
    #      clientes activos en el período 0.

    cohort_data["cohort_size"] = cohort_data.groupby("cohort_month")["active_customers"].transform("first")

    # - `retention_rate`: `active_customers` sobre `cohort_size`.

    cohort_data["retention_rate"] = cohort_data["active_customers"] / cohort_data["cohort_size"]


    #####################################################################################
    ############################# cohort_retention.csv ##################################
    #####################################################################################

    # 1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
    #      `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
    #      `retention_rate`, y una fila por cada combinación cohorte–período
    #      observada, ordenadas por cohorte y período.

    cohort_retention = cohort_data[["cohort_month", "period_index", "active_customers",
                                  "cohort_size", "retention_rate"]]

    cohort_retention = cohort_retention.sort_values(["cohort_month", "period_index"])

    cohort_retention.to_csv(base_dir / "submission" / "cohort_retention.csv", index = False)


    #####################################################################################
    ####################### cohort_retention_heatmap.png ################################
    #####################################################################################

    # 2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
    #      con una fila por cohorte (eje vertical) y una columna por período
    #      (eje horizontal). Muestre los valores como porcentajes. Los períodos
    #      que todavía no se pueden observar para una cohorte no significan
    #      retención cero: déjelos vacíos en el mapa.

    # 1. Crear la matriz con pivot (los periodos sin datos quedan como NaN)

    retention_matrix = cohort_data.pivot(
      index="cohort_month", columns="period_index", values="retention_rate"
    )

    # 2. Generar el mapa de calor básico
    plt.figure(figsize=(10, 6))
    plt.imshow(retention_matrix, cmap="Blues", aspect="auto")

    # 3. Etiquetas de los ejes
    plt.xticks(
      range(len(retention_matrix.columns)),
      labels=retention_matrix.columns
    )
    plt.yticks(
      range(len(retention_matrix.index)),
      labels=retention_matrix.index
    )

    plt.colorbar(label="Retención")
    plt.xlabel("Período")
    plt.ylabel("Cohorte")
    plt.title("Retención por Cohorte")

    # 4. Guardar y cerrar
    plt.tight_layout()
    plt.savefig(base_dir / "submission" / "cohort_retention_heatmap.png")
    plt.close()

    return cohort_retention


if __name__ == "__main__":
    print(build_cohort_analysis())
