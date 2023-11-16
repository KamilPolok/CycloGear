import numpy as np

from ChartView import Chart
from MainWindow import MainWindow

from DbHandler.controller.DBController import ViewSelectItemController
from DbHandler.model.DatabaseHandler import DatabaseHandler
from DbHandler.view.Window import Window

class MainWindowController:
    def __init__(self, model, view: MainWindow):
        self.window = view
        self.data = model

        self.startup()
        self._connectSignalsAndSlots()

    def startup(self):
        # Pass necessary data to view:
        self.window.setData(self.data)
        # Init tabs
        self.window.initTabs()

    def _connectSignalsAndSlots(self):
        # self.window.viewChartBtn.clicked.connect(self.displayChart)
        self.window.tabs[0].SelectMaterialBtn.clicked.connect(self.openMaterialsWindow)
        self.window.tabs[1].updatedBearings1DataSignal.connect(self.openBearings1Window)
        self.window.tabs[1].updatedBearings2DataSignal.connect(self.openBearings2Window)
        self.window.tabs[0].updatedDataSignal.connect(self._calculateInputShaftAttr)
        # self.window.updatedSupportBearingsSignal.connect(self._calculateBearings1Attr)
        # self.window.updatedCycloBearingsSignal.connect(self._calculateBearings2Attr)
        pass

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
        subWindow.itemDataSignal.connect(self.window.tabs[0].updateViewedMaterial)
        subWindow.exec()
    
    def openBearings1Window(self, data):
        self._calculateBearings1Attr(data)
        # # Get acces to the database
        dbHandler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subWindow = Window()
        subWindow.setWindowTitle("Wybór łożyska tocznego")
        # Specify the group name of the tables you want to take for consideration
        tablesGroupName = 'łożyska-wał wejściowy'
        availableTables = dbHandler.getAvailableTables(tablesGroupName)
        # Specify the limits for the group of tables
        limits = dbHandler.getTableItemsFilters(tablesGroupName)
        limits['Dw']['min'] = self.data['ds'][0]
        limits['C']['min'] = self.data['C1'][0]
        # Setup the controller for the subwindow
        viewSelectItemsCtrl = ViewSelectItemController(dbHandler, subWindow, availableTables, limits)
        subWindow.itemDataSignal.connect(self.window.tabs[1].updateViewedBearing1)
        subWindow.exec()
    
    def openBearings2Window(self, data):
        self._calculateBearings2Attr(data)
        # # Get acces to the database
        dbHandler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subWindow = Window()
        subWindow.setWindowTitle("Wybór łożyska tocznego")
        # Specify the group name of the tables you want to take for consideration
        tablesGroupName = 'łożyska-tarcza'
        availableTables = dbHandler.getAvailableTables(tablesGroupName)
        # Specify the limits for the group of tables
        limits = dbHandler.getTableItemsFilters(tablesGroupName)
        limits['Dw']['min'] = self.data['de'][0]
        limits['C']['min'] = self.data['C2'][0]
        # Setup the controller for the subwindow
        viewSelectItemsCtrl = ViewSelectItemController(dbHandler, subWindow, availableTables, limits)
        subWindow.itemDataSignal.connect(self.window.tabs[1].updateViewedBearing2)
        subWindow.exec()

    def _calculateBearings1Attr(self, data):
        if data is not None:
            for key, value in data.items():
                    if key in self.data:
                        self.data[key] = value

        nwe = self.data['nwe'][0]
        lh = self.data['Lh1'][0]
        fd = self.data['fd1'][0]
        ft = self.data['ft1'][0]
        p = 3.0

        ra = self.data['Ra'][0]
        rb = self.data['Rb'][0]

        l = 60*lh*nwe/np.power(10,6)
        c = ra*np.power(l,1/p)*ft/fd

        self.data['Lt1'][0] = l
        self.data['C1'][0] = c
    
        print(self.data)
    
    def _calculateBearings2Attr(self, data):
        if data is not None:
            for key, value in data.items():
                    if key in self.data:
                        self.data[key] = value

        nwe = self.data['nwe'][0]
        lh = self.data['Lh2'][0]
        fd = self.data['fd2'][0]
        ft = self.data['ft2'][0]
        p = 3.0

        f1 = self.data['F1'][0]
        f2 = self.data['F2'][0]

        l = 60*lh*nwe/np.power(10,6)
        c = f1*np.power(l,1/p)*ft/fd

        self.data['Lt2'][0] = l
        self.data['C2'][0] = c

    def _calculateInputShaftAttr(self, data = None):
        if data is not None:
            for key, value in data.items():
                    if key in self.data:
                        self.data[key] = value

        L = self.data['L'][0]
        LA = self.data['LA'][0]
        LB = self.data['LB'][0]
        L1 = self.data['L1'][0]
        L2 = self.data['L2'][0]
        F1 = self.data['F1'][0]
        F2 = self.data['F2'][0]
        Mo = self.data['Mo'][0]
        Zgo = self.data['Materiał']['Zgo'][0]
        xz = self.data['xz'][0]
        e = self.data['e'][0]

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

        # Safe the calculated parameters
        self.data['ds'][0] = max(self.d)
        self.data['de'][0] = max(self.d) + 2 * e
        self.data['Ra'][0] = Ra
        self.data['Rb'][0] = Rb

        print("Input shaft parameters CALCULATED")
        print(self.data)

