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
        optionsRowsColumn = ft.Column()
        for attribute, attribute_limits in self.limits.items():
            option = Option(attribute, attribute_limits)
            self.options.append(option)
            optionsRowsColumn.controls.append(option)
        
        updateResultsButton = ft.Row(controls = [ft.ElevatedButton(text = "FILTRUJ",
                                                                        expand = True,
                                                                        style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius=10)),
                                                                        on_click = self.updateResultsClick)],
                                          alignment=ft.MainAxisAlignment.CENTER)
        
        self.dbList = ListViewer(self.dbHandler.get_filtered_table(self.limits), self.selectItem)
        
        self.selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self.selectedItem}")])

        self.wrappingColumn = ft.Column(controls=[optionsRowsColumn,
                                               updateResultsButton,
                                               self.dbList,
                                               self.selectedItemRow])
        
        return self.wrappingColumn
    
    def selectItem(self, dbRow):
        code = dbRow[0]
        self.selectedItem = self.dbHandler.get_single_position(code)

        self.wrappingColumn.controls.remove(self.selectedItemRow)
        self.selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self.selectedItem}")])
        self.wrappingColumn.controls.insert(3, self.selectedItemRow)

        self.update()
    
    def updateResultsClick(self, e):
        for option in self.options:
            optionLimits = option.getLimits()
            for index, limit in enumerate(self.limits[option.optionName]):
                if(optionLimits[index]):
                    self.limits[option.optionName][limit] = optionLimits[index]
                else:
                    self.limits[option.optionName][limit] = 0

        self.wrappingColumn.controls.remove(self.dbList)
        self.dbList = ListViewer(self.dbHandler.get_filtered_table(self.limits), self.selectItem)
        self.wrappingColumn.controls.insert(2, self.dbList)
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
        for index, dbRow in self.df.astype('str').iterrows():
            elementsRowsCol.controls.append(self._createClickableRow(dbRow))

        wrappingColumn = ft.Column(controls=[headersRow,
                                          elementsRowsCol])
            
        return wrappingColumn
    
    def _createRow(self, dbRow):
        listRow = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY)
        for element in dbRow :
            listRow.controls.append(ft.Column(width = 100,
                                          controls=[ft.Text(element)]))

        return listRow

    def _createClickableRow(self, dbRow):
        listRow = self._createRow(dbRow)
        clickableContainer = ft.Container(content=listRow,
                                          ink=True,
                                          on_click=lambda e: self.selectItemClick(dbRow, e))

        return clickableContainer
    
    def selectItemClick(self, dbRow, e):
        self.selectItem(dbRow)
    
class Option(ft.UserControl):
    def __init__(self, optionName, limits):
        super().__init__()
        self.optionName = optionName
        self.limits = limits
        self.limitTextFieldsList = []
    
    def build(self):
        optionNameColumn = ft.Column(width = 200,
                               controls=[ft.Text(self.optionName)])
        
        row = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                     controls=[optionNameColumn])
        
        for limit, value in self.limits.items():
            limitTextField = ft.TextField(label=limit,
                                          dense=True,
                                          text_size=14)
            limitTextFieldColumn = ft.Column(width = 100,
                                             controls = [limitTextField])
            
            row.controls.append(limitTextFieldColumn)

            self.limitTextFieldsList.append(limitTextField)

        return row

    def getLimits(self):
        #todo: move the functionality of changing the limits array from OptionsManager updateResultsClick to here in getLimits
        limits = []
        for limitTextField in self.limitTextFieldsList:
            number = self._convertToNumber(limitTextField.value)
            if number <= 0:
                number = 0
                limitTextField.value=""
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