import numpy as np
from sympy import symbols, Piecewise

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
        self.window.tabs[0].SelectMaterialBtn.clicked.connect(self.openMaterialsWindow)
        self.window.tabs[1].updatedBearings1DataSignal.connect(self.openBearings1Window)
        self.window.tabs[1].updatedBearings2DataSignal.connect(self.openBearings2Window)
        self.window.tabs[0].updatedDataSignal.connect(self._calculateInputShaftAttr)
        self.window.tabs[1].updatedDataSignal.connect(self._updateBearingsData)
        # self.window.updatedSupportBearingsSignal.connect(self._calculateBearings1Attr)
        # self.window.updatedCycloBearingsSignal.connect(self._calculateBearings2Attr)
        pass

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
        limits['Dw']['min'] = self.data['dsc'][0]
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
        limits['Dw']['min'] = self.data['dec'][0]
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
        c = ra*np.power(l,1/p)*ft/fd/ 1000 # kN

        self.data['Lt1'][0] = l
        self.data['C1'][0] = c
    
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

        l = 60 * lh * nwe / np.power(10, 6)
        c = f1 * np.power(l, 1 / p) * ft / fd/ 1000 # kN

        self.data['Lt2'][0] = l
        self.data['C2'][0] = c
    
    def _updateBearingsData(self, data):
        if data is not None:
            for key, value in data.items():
                if key in self.data:
                    self.data[key] = value

    def calcMg(self, L, LA, LB, L1, L2, F1, F2, Ra, Rb):
        z = symbols('z')
        

    def calcMs(self, L, L2, Mwe):
        z = symbols('z')
       
         
    def _calculateInputShaftAttr(self, data):
        # Save received data 
        for key, value in data.items():
                if key in self.data:
                    self.data[key] = value

        # Get data
        L = self.data['L'][0]
        LA = self.data['LA'][0]
        LB = self.data['LB'][0]
        L1 = self.data['L1'][0]
        L2 = self.data['L2'][0]
        F1 = self.data['F1'][0]
        F2 = self.data['F2'][0]
        Mwe = self.data['Mwe'][0]
        Zgo = self.data['Materiał']['Zgo'][0]
        xz = self.data['xz'][0]
        e = self.data['e'][0]

        # Calculate support reactions
        Rb = (-F1*L1-F2*L2)/(LB-LA)
        Ra = -F1-F2-Rb

        # Create Force and reaction list
        F = [Ra, F1, F2, Rb]

        # Create z arguments
        key_points = [0, LA, L1, L2, LB, L]
        z = symbols('z')
        zVals = np.union1d(key_points, np.linspace(0, L, 50))

        # Calculate bending moment Mg
        # Calculate subfunctions of bending moment
        Mg0_A = 0                                                                           # for  0 <= x < LA
        MgA_1 = -Ra * (z - LA) * 0.001                                                      # for LA <= z < L1
        Mg1_2 = (-Ra * (z - LA) - F1 * (z - L1)) * 0.001                                    # for L1 <= z < L2
        Mg2_B = (-Ra * (z - LA) - F1 * (z - L1) - F2 * (z - L2) ) * 0.001                   # for L2 <= z < LB
        MgB_K = (-Ra * (z - LA) - F1 * (z - L1) - F2 * (z - L2) - Rb * (z - LB) ) * 0.001   # for LB <= z <= L
        # Create the piecewise function - connect the subfunctions in one function
        MgFunction = Piecewise(
            (Mg0_A, z < LA),
            (MgA_1, z < L1),
            (Mg1_2, z < L2),
            (Mg2_B, z < LB),
            (MgB_K, z <= L)
            )
        # Create Mg values
        Mg = [MgFunction.subs(z, val).evalf() for val in zVals]
        Mg = np.array([round(float(val), 2) for val in Mg])

        # Calculate torque Ms
        # Calculate subfunctions of torque Ms
        MsFunction = Piecewise(
            (Mwe, z < L2),
            (0, z <= L)
        )
        # Create Ms values
        Ms = [MsFunction.subs(z, val).evalf() for val in zVals]
        Ms = np.array([round(float(val), 2) for val in Ms]) 

        # Calculate equivalent moment Mz
        reductionFactor = 2 * np.sqrt(3)
        Mz = np.sqrt(np.power(Mg, 2) + np.power(reductionFactor / 2 * Ms, 2))
        Mz = np.array([round(float(val), 2) for val in Mz])

        # Calulate shaft diameter d
        kgo = Zgo/xz
        d = np.power(32*Mz/(np.pi*kgo*1000000), 1/3)*1000
        d = np.array([round(float(val), 2) for val in d])

        # Safe the calculated parameters
        self.data['dsc'][0] = max(d)
        self.data['dec'][0] = max(d) + 2 * e
        self.data['Ra'][0] = Ra
        self.data['Rb'][0] = Rb

        # Set chart data
        self.chartData = {'z' : zVals, 
                          'F' : F,
                          'Mg' : Mg, 
                          'Ms' : Ms,
                          'Mz' : Mz,
                          'd' : d, 
                          }
        
        self.window.setChartData(self.chartData)
