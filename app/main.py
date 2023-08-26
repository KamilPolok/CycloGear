import flet as ft
import pandas as pd
from ast import literal_eval
import re

from database import DatabaseHandler

class UIListManager(ft.UserControl):
    def __init__(self):
        super().__init__()
        self._dbHandler = DatabaseHandler()
        self._limits = {attribute:{"min": 0, "max": 0} for attribute in self._dbHandler.getAttributes() }

        self._options = []
        self._selectedItem = []

    def build(self):
        optionsRowsColumn = ft.Column()
        for attribute, attributeLimits in self._limits.items():
            option = Option(attribute, attributeLimits)
            self._options.append(option)
            optionsRowsColumn.controls.append(option)
        
        updateResultsButton = ft.Row(controls = [ft.ElevatedButton(text = "FILTRUJ",
                                                                   expand = True,
                                                                   style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius=10)),
                                                                   on_click = self.updateResultsEvent)],
                                                                   alignment = ft.MainAxisAlignment.CENTER)
        
        self._dbList = ListViewer(self._dbHandler.getFilteredResults(self._limits), self.selectItem)
        
        self._selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self._selectedItem}")])

        self._wrappingColumn = ft.Column(controls = [optionsRowsColumn,
                                                    updateResultsButton,
                                                    self._dbList,
                                                    self._selectedItemRow])
        
        return self._wrappingColumn
    
    def selectItem(self, dbRow):
        code = dbRow[0]
        self._selectedItem = self._dbHandler.getSnglePosition(code)

        self._wrappingColumn.controls.remove(self._selectedItemRow)
        self._selectedItemRow = ft.Row(controls = [ft.Text(f"WYBRANY ELEMENT: {self._selectedItem}")])
        self._wrappingColumn.controls.insert(3, self._selectedItemRow)

        self.update()
    
    def updateResultsEvent(self, e):
        for option in self._options:
            self._limits[option._optionName] = option.getOptionLimits()

        self._wrappingColumn.controls.remove(self._dbList)
        self._dbList = ListViewer(self._dbHandler.getFilteredResults(self._limits), self.selectItem)
        self._wrappingColumn.controls.insert(2, self._dbList)
        self.update()

class ListViewer(ft.UserControl):
    def __init__(self, df, selectItem):
        super().__init__()
        self._selectItem = selectItem
        self._df = df
        
    def build(self):
        headersRow = self._createRow(self._df.columns)

        elementsRowsCol = ft.Column(height = 200,
                                    scroll = ft.ScrollMode.ALWAYS)
        
        for index, dbRow in self._df.astype('str').iterrows():
            elementsRowsCol.controls.append(self._createClickableRow(dbRow))

        wrappingColumn = ft.Column(controls = [headersRow,
                                               elementsRowsCol])
            
        return wrappingColumn
    
    def _createRow(self, dbRow):
        row = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY)
        for element in dbRow :
            row.controls.append(ft.Column(width = 100,
                                          controls = [ft.Text(element)]))

        return row

    def _createClickableRow(self, dbRow):
        clickableContainer = ft.Container(content=self._createRow(dbRow),
                                          ink = True,
                                          on_click=lambda e: self.selectItemEvent(dbRow, e))

        return clickableContainer
    
    def selectItemEvent(self, dbRow, e):
        self._selectItem(dbRow)
    
class Option(ft.UserControl):
    def __init__(self, optionName, optionLimits):
        super().__init__()
        self._optionName = optionName
        self._optionLimits = optionLimits
        self._limitTextFieldsDict = {}
    
    def build(self):
        optionNameColumn = ft.Column(width = 200,
                                     controls = [ft.Text(self._optionName)])
        
        row = ft.Row(alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                     controls = [optionNameColumn])
        
        for limit, value in self._optionLimits.items():
            limitTextField = ft.TextField(label = limit,
                                          dense = True,
                                          text_size = 14,
                                          on_blur = self.onBlurEvent
                                          )
            
            limitTextFieldColumn = ft.Column(width = 100,
                                             controls = [limitTextField])
            
            row.controls.append(limitTextFieldColumn)

            self._limitTextFieldsDict[limit] = limitTextField

        return row

    def getOptionLimits(self):
        for key, limitTextField in self._limitTextFieldsDict.items():
            number = literal_eval(limitTextField.value) if limitTextField.value else 0
            self._optionLimits[key] = number

        return self._optionLimits
    
    def onBlurEvent(self, e):
        if re.match(r'^\s*(?!0+(\.0*)?$)\d+(\.\d+)?\s*$', e.control.value):
            maxLength = 8
            e.control.value = e.control.value.strip()[:maxLength]
        else:
            e.control.value = ""
        e.control.update()

def main(page: ft.Page):
    page.title="DATABASE SAMPLE"
    page.window_width=825
    page.window_height=800
    page.bgcolor="WHITE"

    uiListManager = UIListManager()
    page.add(uiListManager)
ft.app(target=main)