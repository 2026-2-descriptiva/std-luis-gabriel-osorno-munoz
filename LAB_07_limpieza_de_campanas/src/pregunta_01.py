import pandas as pd
from pathlib import Path
import numpy as np





#####################################################################################################
##################################### Clean functions 1 #############################################
#####################################################################################################

def cleaner_guiones1(series):

    data = series.str.replace("-", "_", regex=False)

    return data

def cleaner_puntos_guiones1(series):
    
    data = series.str.replace(".", "_", regex = False)

    return data

def cleaner_puntos_nothing1(series):
    
    data = series.str.replace(".", "", regex = False)

    return data


def cleaner_unknow1(series):

    data = series.replace("unknown", None)

    return data

def cleaner_binario1(series):

    data = (series=="yes").astype(int)

    return data

#####################################################################################################
#################################### Dataset 1 ######################################################
#####################################################################################################

def clean_job1(data):

    data.loc[:, "job"] = cleaner_puntos_nothing1(data["job"])
    data.loc[:, "job"] = cleaner_guiones1(data["job"])

    return data

def clean_education1(data):

    data.loc[:, "education"] = cleaner_puntos_guiones1(data["education"])
    data.loc[:, "education"] = cleaner_unknow1(data["education"])

    return data

def clean_credit_default1(data):
    
    data.loc[:, "credit_default"] = cleaner_binario1(data["credit_default"])    

    return data

def clean_mortgage1(data):
    
    data.loc[:, "mortgage"] = cleaner_binario1(data["mortgage"])    

    return data

#####################################################################################################
##################################### Clean functions 2 #############################################
#####################################################################################################

def cleaner_binario2(series):

    data = (series == "success").astype(int)

    return data

def cleaner_fecha2(series):

    data = series

    return data

#####################################################################################################
#################################### Dataset 2 ######################################################
#####################################################################################################


def clean_previous_outcome2(data):

    data.loc[:, "previous_outcome"] = cleaner_binario2(data["previous_outcome"])

    return data

def clean_campaign_outcome2(data):

    data.loc[:,"campaign_outcome"] = cleaner_binario1(data["campaign_outcome"])

    return data

#  - Construya `last_contact_date` a partir de las columnas `month` y
#    `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

def clean_last_contact_date2(data):

    data.loc[:,"month"] = pd.to_datetime(data["month"], format="%b").dt.strftime("%m")

    data["day"] = data["day"].astype(str).str.zfill(2)

    data["last_contact_date"] = "2022"+ "-" + data["month"] + "-" + data["day"]

    return data


















def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    # Lectura de los 10 archivos datset

    Base_dir = Path(__file__).parent.parent

    file = Base_dir / "data"

    archivos = list(file.glob("bank-marketing-campaing*"))

    data = pd.concat([pd.read_csv(f, compression="gzip", sep=",") for f in archivos], ignore_index=True)


    #####################################################################################################
    #################################### Dataset 1 ######################################################
    #####################################################################################################

    # 1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
    #    `credit_default` y `mortgage`.

    columns_client = ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]

    dataset_client  = data.copy()

    dataset_client = dataset_client[columns_client]

    #   - En `job`, elimine los puntos y cambie los guiones por guiones bajos.

    dataset_client = clean_job1(dataset_client)

    #   - En `education`, cambie los puntos por guiones bajos y deje el valor 
    #     `unknown` como faltante.

    dataset_client = clean_education1(dataset_client)  

    #   - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
    #     en cualquier otro caso.

    dataset_client = clean_credit_default1(dataset_client)

    dataset_client = clean_mortgage1(dataset_client)

    # Guardado del dataset

    file_output_client = Base_dir / "submission" / "client.csv"

    dataset_client.to_csv(file_output_client, index=False)


    #####################################################################################################
    #################################### Dataset 2 ######################################################
    #####################################################################################################

    # 2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
    #    `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
    #    `last_contact_date`.

    columns_campaign_firt = ["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts",
                             "previous_outcome", "campaign_outcome", "month", "day"]

    dataset_campaing = data.copy()

    dataset_campaing = dataset_campaing[columns_campaign_firt]

    #  - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en cualquier otro caso.

    dataset_campaing = clean_previous_outcome2(dataset_campaing)

    #  - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
    #    cualquier otro caso.

    dataset_campaing = clean_campaign_outcome2(dataset_campaing)

    #  - Construya `last_contact_date` a partir de las columnas `month` y
    #    `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    dataset_campaing = clean_last_contact_date2(dataset_campaing)

    # Dataset final 

    columns_campaign_end = ["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts",
                                 "previous_outcome", "campaign_outcome", "last_contact_date"]

    dataset_campaing = dataset_campaing[columns_campaign_end]

    file_output_camping = Base_dir / "submission" / "campaign.csv"

    dataset_campaing.to_csv(file_output_camping, index=False)


    #####################################################################################################
    #################################### Dataset 3 ######################################################
    #####################################################################################################

    # 3. `economics.csv`: `client_id`, `cons_price_idx` y
    #    `euribor_three_months`.

    columns_economics = ["client_id", "cons_price_idx", "euribor_three_months"]

    dataset_economics = data.copy()

    dataset_economics = dataset_economics[columns_economics]

    file_output_economics = Base_dir / "submission" / "economics.csv"

    dataset_economics.to_csv(file_output_economics, index = False)

    return dataset_client, dataset_campaing, dataset_economics

if __name__ == "__main__":
    print(clean_campaign_data())




