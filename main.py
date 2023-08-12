import flet as ft
import pandas as pd

from database import DatabaseHandler

class OptionsManager(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.dbHandler = DatabaseHandler()
        self.attributes = self.dbHandler.get_attributes()
        self.limits = {attribute:{"min": 0, "max": 0} for attribute in self.attributes }

        self.options = []
        self.selectedItem = []

    def build(self):

        self.updateResultsButton = ft.Row(controls = [ft.ElevatedButton(text = "FILTRUJ",
                                                                        expand = True,
                                                                        style = ft.ButtonStyle(
                                                                            shape = ft.RoundedRectangleBorder(radius=10)),
                                                                        on_click = self.updateResultsClick)],
                                          alignment=ft.MainAxisAlignment.CENTER)
        self.selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self.selectedItem}")])

        self.wrappingCol = ft.Column()
        self.optionsRowsCol = ft.Column()
        self.dbList = ListViewer(self.dbHandler.get_filtered_table(self.limits), self.selectItem)

        for attribute, attribute_limits in self.limits.items():
            option = Option(attribute, attribute_limits)
            self.options.append(option)
            self.optionsRowsCol.controls.append(option)

        self.wrappingCol.controls.append(self.optionsRowsCol)
        self.wrappingCol.controls.append(self.updateResultsButton)
        self.wrappingCol.controls.append(self.dbList)
        self.wrappingCol.controls.append(self.selectedItemRow)
        return self.wrappingCol
    
    def selectItem(self, row):
        self.selectedItem = self.dbHandler.get_single_position(row[0])
        self.wrappingCol.controls.remove(self.selectedItemRow)
        self.selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self.selectedItem}")])
        self.wrappingCol.controls.insert(3, self.selectedItemRow)
        print(self.selectedItem)
        self.update()
    
    def updateResultsClick(self, e):
        for option in self.options:
            optionLimits = option.getLimits()
            for index, limit in enumerate(self.limits[option.optionName]):
                if(optionLimits[index]):
                    self.limits[option.optionName][limit] = optionLimits[index]
                else:
                    self.limits[option.optionName][limit] = 0
        self.wrappingCol.controls.remove(self.dbList)
        self.dbList = ListViewer(self.dbHandler.get_filtered_table(self.limits), self.selectItem)
        self.wrappingCol.controls.insert(2, self.dbList)
        self.update()

class ListViewer(ft.UserControl):
    def __init__(self, df, selectItem):
        super().__init__()
        self.selectItem = selectItem
        self.df = df
        
    def build(self):
        headersRow = self._createRow(self.df.columns)
        elementsRowsCol = ft.Column(
            height=200,
            scroll=ft.ScrollMode.ALWAYS,
        )
        for index, row in self.df.astype('str').iterrows():
            elementsRowsCol.controls.append(self._createClickableRow(row))

        wrappingCol = ft.Column(controls=[headersRow, elementsRowsCol])        
        return wrappingCol
    
    def _createRow(self, row):
        r = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY)
        for element in row :
            r.controls.append(ft.Column(width = 100, controls=[ft.Text(element)]))

        return r

    def _createClickableRow(self, row):
        r = self._createRow(row)
        ct = ft.Container(
                    content=r,
                    ink=True,
                    on_click=lambda e: self.selectItemClick(row, e)
        )

        return ct
    
    def selectItemClick(self, row, e):
        self.selectItem(row)
    
class Option(ft.UserControl):
    def __init__(self, optionName, limits):
        super().__init__()
        self.optionName = optionName
        self.limits = limits
        self.textFieldsList = []
    
    def build(self):
        row = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY)
        row.controls.append(ft.Column(width = 200, controls=[ft.Text(self.optionName)]))
        for limit, value in self.limits.items():
            textField = ft.TextField(label=limit,
                                     dense=True,
                                     text_size=14)
            row.controls.append(ft.Column(width = 100,
                                          controls=[textField]))
            self.textFieldsList.append(textField)
        return row

    def getLimits(self):
        #todo: move the functionality of changing the limits array from OptionsManager updateResultsClick to here in getLimits
        limits = []
        for textField in self.textFieldsList:
            number = self._convertToNumber(textField.value)
            if number <= 0:
                number = 0
                textField.value=""
            limits.append(number)
        self.update()
        return limits
    
    def _convertToNumber(self, string):
        #todo: use Regex to impelement type safety instead exceptions
        try:
            number = int(string)
        except ValueError:  
            try:
                number = float(string)
            except ValueError:
                number = 0
        return number

def main(page: ft.Page):
    page.title="DATABASE SAMPLE"
    page.window_width=825
    page.window_height=800
    page.bgcolor="WHITE"

    optionsManager = OptionsManager()
    page.add(optionsManager)
ft.app(target=main)