import pandas as pd
from pathlib import Path
import numpy as np


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
   """
   Una cadena de suministros de oficina vende mucho, pero la gerencia
   sospecha que parte de esas ventas no deja utilidad. El archivo
   `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
   el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
   (`Profit`), el descuento aplicado (`Discount`, como proporción), el
   segmento del cliente (`Customer Segment`) y la categoría del producto
   (`Product Category`). Una utilidad negativa significa que la línea se
   vendió con pérdida.

   Use estas definiciones:

   - Margen (`profit_margin`): utilidad sobre ventas.
   - Línea con pérdida: una línea cuya utilidad es negativa.
   - `loss_line_rate`: la proporción de líneas con pérdida.
   - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
   - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

   Genere tres archivos en `submission/`, sin el índice de Pandas y con las
   columnas en el orden indicado:

   1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
      líneas), `orders` (pedidos distintos), `sales`, `profit`,
      `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
      `loss_line_rate` y `lost_profit`.

   2. `discount_summary.csv`, con una fila por rango de descuento, en el
      orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
      `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

   3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
      que más utilidad pierden: `Customer Segment`, `Product Category`,
      `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
      solamente segmentos con al menos 100 líneas y ordénelos por
      `lost_profit` de mayor a menor.

   La función también debe retornar las tres tablas, en el mismo orden.

   Ejemplo del formato de `discount_summary.csv`:

      discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
      0%,166,170539.05,29472.3789,0.1728,0.488,...
      ...
   """


   base_dir = Path(__file__).parent.parent

   archivo = base_dir / "data" / "superstore_orders.csv.gz"

   data = pd.read_csv(archivo, compression="gzip", sep=";")


   #############################################################################
   ############################ Limpiar el dataset #############################
   #############################################################################

   data["Sales"] = data["Sales"].astype(str).str.replace(",", ".", regex=False).astype(float)

   data["Profit"] = data["Profit"].astype(str).str.replace(",", ".", regex=False).astype(float)


   #############################################################################
   ##################### profitability_summary.csv #############################
   #############################################################################

   ##    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
   ##   líneas), `orders` (pedidos distintos), `sales`, `profit`,
   ##   `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
   ##   `loss_line_rate` y `lost_profit`.

   lines_profitability = data.shape[0]
   orders_profitability = data["Order ID"].nunique()
   sales_profitability = data["Sales"].sum()
   profit_profitability = data["Profit"].sum()
   profit_margin_profitability = profit_profitability/sales_profitability
   data["loss_lines"] = (data["Profit"]<0)
   loss_lines_profitability = data["loss_lines"].sum()
   loss_line_rate_profitability = loss_lines_profitability / len(data["Profit"])
   lost_profit_profitability = data.loc[data["Profit"] < 0, "Profit"].sum()*(-1)

   profitability_summary = pd.DataFrame([{
      "lines": lines_profitability,
      "orders": orders_profitability,
      "sales": sales_profitability,
      "profit": profit_profitability,
      "profit_margin": profit_margin_profitability,
      "loss_lines": loss_lines_profitability,
      "loss_line_rate": loss_line_rate_profitability,
      "lost_profit": lost_profit_profitability
         }])

   profitability_summary.to_csv(base_dir / "submission" /"profitability_summary.csv", index= False)

   #############################################################################
   ########################## discount_summary.csv #############################
   #############################################################################

   # 2. `discount_summary.csv`, con una fila por rango de descuento, en el
   #   orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
   #   `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

   data["discount_band"] = pd.cut(data["Discount"].astype(str).str.replace(",", ".").astype(float),
                                 labels=["0%", "1%-5%", "6%-10%", "más de 10%"],
                                 bins=[-np.inf, 0, 0.05, 0.10, np.inf], right=True)

   discount_summary = data.groupby("discount_band", as_index=False, observed=False).agg(
      lines = ("discount_band", "count"),
      sales = ("Sales", "sum"),
      profit = ("Profit", "sum"),
      loss_line = ("loss_lines", "sum"),
      lost_profit = ("Profit", lambda x: x[x<0].sum()*(-1)))

   discount_summary["profit_margin"] = discount_summary["profit"]/discount_summary["sales"]

   discount_summary["loss_line_rate"] = discount_summary["loss_line"]/discount_summary["lines"]

   discount_summary = discount_summary.drop(columns="loss_line")

   column_order = ["discount_band", "lines", "sales", "profit",
                  "profit_margin", "loss_line_rate", "lost_profit"]

   discount_summary = discount_summary[column_order]

   discount_summary.to_csv(base_dir / "submission" / "discount_summary.csv", index=False)

   #############################################################################
   ######################### priority_segments.csv #############################
   #############################################################################

   # 3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
   #      que más utilidad pierden: `Customer Segment`, `Product Category`,
   #      `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
   #      solamente segmentos con al menos 100 líneas y ordénelos por
   #      `lost_profit` de mayor a menor.

   customer_segment_priority = data.groupby(["Customer Segment", "Product Category"], as_index=False).agg(
      lines = ("Order ID", "count"),
      sales = ("Sales", "sum"),
      profit = ("Profit", "sum"),
      lost_profit = ("Profit", lambda x: x[x<0].sum()*(-1)))

   customer_segment_priority["profit_margin"] = customer_segment_priority["profit"]/customer_segment_priority["sales"]

   customer_segment_priority = customer_segment_priority[["Customer Segment", "Product Category", "lines",
                                                         "sales", "profit", "profit_margin", "lost_profit"]]

   customer_segment_priority = customer_segment_priority[customer_segment_priority["lines"] >= 100]

   customer_segment_priority = customer_segment_priority.sort_values(by="lost_profit", ascending=False).head(5)

   customer_segment_priority.to_csv(base_dir / "submission" / "priority_segments.csv", index = False)
   
   return profitability_summary, discount_summary, customer_segment_priority
   #return profitability_summary



if __name__ == "__main__":
   print(pregunta_01())