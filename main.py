import flet as ft
import pandas as pd

import flet_utility
from database import DatabaseHandler

positions = [ 'D_wewnetrzna', 'D_zewnetrzna', 'B', 'C', 'C0', 'predkosc_referencyjna', 'predkosc_dopuszczalna']
limits = {position:{"min": 0, "max": 0} for position in positions }

# handler = DatabaseHandler()


# limits['D_wewnetrzna']['min'] = 35
# limits['predkosc_referencyjna']['max'] = 22000 


# table = handler.get_filtered_table(limits)

# # for row in table:
# #     print(row)

# bearing = handler.get_single_position(6003)
# print(bearing)

def viewBearingsTable(page: ft.Page, db_handler: DatabaseHandler):

    df = db_handler.get_filtered_table(limits)
    datatable = ft.DataTable(
        columns=flet_utility.headers(df),
        rows=flet_utility.rows(df))
    
    lv = ft.ListView(expand=True, spacing=10)
    lv.controls.append(datatable)

    page.controls.append(lv)

def viewOptions(page: ft.Page, db_handler: DatabaseHandler):
    c = ft.Container(
        content=ft.ElevatedButton("Elevated Button in Container"),
        bgcolor=ft.colors.YELLOW,
        padding=5,
    )
    page.controls.append(c)

def main(page: ft.Page):

    db_handler = DatabaseHandler()
    page.title = "PRZEŁADNIA CYKLOIDALNA"
    viewOptions(page, db_handler)
    viewBearingsTable(page, db_handler)
    page.update()

ft.app(target=main)
