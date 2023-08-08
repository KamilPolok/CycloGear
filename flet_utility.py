import flet as ft
import pandas as pd

def headers(df : pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header), numeric=True) for header in df.columns]

def rows(df : pd.DataFrame) -> list:
    rows = []
    for index, row in df.astype('str').iterrows():
        rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows