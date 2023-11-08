import numpy as np

from ChartView import Chart

from DbHandler.controller.DBController import ViewSelectItemController
from DbHandler.model.DatabaseHandler import DatabaseHandler
from DbHandler.view.Window import Window

class MainWindowController:
    def __init__(self, model, view):
        self.window = view
        self.data = model

        self.material = {'Oznaczenie': 'Stal C45',
                'Rm': [600, 'MPa'],
                'Re': [340, 'MPa'],
                'Zgj': [460,'MPa'],
                'Zgo': [250, 'MPa'],
                'Zsj': [300, 'MPa'],
                'Zso': [150, 'MPa'],
                'E': [2100000, 'MPa'],
                'G': [80750, 'MPa'],
                'g': [7860, 'kg/m^3'],
            }

        self.startup()
        self._connectSignalsAndSlots()

    def startup(self):
        # Pass necessary data to view:
        self.window.setData(self.data)
        # Init view
        self.window.viewDataAcqSection()
        self.window.viewDataDispSection(self.data)

    def _connectSignalsAndSlots(self):
        self.window.updateDataBtn.clicked.connect(self._performCalculations)
        self.window.viewChartBtn.clicked.connect(self.displayChart)
        self.window.SelectMaterialBtn.clicked.connect(self.openMaterialsWindow)

    def displayChart(self):
        self.chart = Chart(self.z, self.F, self.Mg, self.Ms, self.Mz, self.d)
        self.chart.exec()

    def openMaterialsWindow(self):
        # # Get acces to the database
        dbHandler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subWindow = Window()
        subWindow.setWindowTitle("Wybór materiału")
        # Specify the group name of the tables you want to take for consideration
        tablesGroupName = 'wał bierny: materiały'
        availableTables = dbHandler.getAvailableTables(tablesGroupName)
        # Specify the limits for the group of tables
        limits = dbHandler.getTableItemsFilters(tablesGroupName)
        # Setup the controller for the subwindow
        viewSelectItemsCtrl = ViewSelectItemController(dbHandler, subWindow, availableTables, limits)
        subWindow.itemDataSignal.connect(self.window.updateViewedMaterial)
        subWindow.exec()

    def _performCalculations(self):
        self.data = self.window.getData()
        print(self.data)
        L = self.data['L'][0]
        LA = self.data['LA'][0]
        LB = self.data['LB'][0]
        L1 = self.data['L1'][0]
        L2 = self.data['L2'][0]
        F1 = self.data['F1'][0]
        F2 = self.data['F2'][0]
        Mo = self.data['Mo'][0]
        Zgo = self.material['Zgo'][0]
        xz = self.data['xz'][0]

        self.z = [0, LA, L1, L2, LB, L]


        # Reakcje podporowe
        Rb = (-F1*L1-F2*L2)/(LB-LA)
        Ra = -F1-F2-Rb

        self.F = [0, Ra, F1, F2, Rb, 0]
        # Momenty gnące
        MgP = 0
        MgA = 0*(LA)
        Mg1 = -Ra*(L1-LA)
        Mg2 = -Ra*(L2-LA)-F1*(L2-L1)
        MgB = -Ra*(LB-LA)-F1*(LB-L1)-F2*(LB-L2)
        MgK = -Ra*(L-LA)-F1*(L-L1)-F2*(L-L2)-Rb*(L-LB)

        self.Mg = np.array([MgP, MgA, Mg1, Mg2,MgB, MgK])
        # Momenty skręcające
        self.Ms = np.array([Mo, Mo, Mo, Mo, 0, 0])
        # Momenty zastępcze
        wsp_redukcyjny = 2 * np.sqrt(3)

        self.Mz = np.sqrt(np.power(self.Mg, 2) + np.power(wsp_redukcyjny / 2 * self.Ms, 2))
        # Średnica wału
        kgo = Zgo/xz
        self.d = np.power(32*self.Mz/(np.pi*kgo*1000000), 1/3)*1000
