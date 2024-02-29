
from PyQt6.QtCore import pyqtSignal, QObject

class Mediator(QObject):
    shaftDesigningFinished = pyqtSignal()
    updateComponentData = pyqtSignal(int, dict)

    selectMaterial = pyqtSignal()
    selectSupportABearing = pyqtSignal(dict)
    selectSupportBBearing = pyqtSignal(dict)
    selectCentralBearing = pyqtSignal(dict)

    selectSupportABearingRollingElement = pyqtSignal(dict)
    selectSupportBBearingRollingElement = pyqtSignal(dict)
    selectCentralBearingRollingElement = pyqtSignal(dict)

    def emit_shaft_designing_finished(self):
        self.shaftDesigningFinished.emit()
    
    def update_component_data(self, tab_id: int, data: dict):
        self.updateComponentData.emit(tab_id, data)

    def select_material(self):
        self.selectMaterial.emit()
    
    def select_support_A_bearing(self, data: dict):
        self.selectSupportABearing.emit(data)
        
    def select_support_B_bearing(self, data: dict):
        self.selectSupportBBearing.emit(data)
        
    def select_central_bearing(self, data: dict):
        self.selectCentralBearing.emit(data)

    def select_support_A_bearing_rolling_element(self, data: dict):
        self.selectSupportABearingRollingElement.emit(data)
        
    def select_support_B_bearing_rolling_element(self, data: dict):
        self.selectSupportBBearingRollingElement.emit(data)
        
    def select_central_bearing_rolling_element(self, data: dict):
        self.selectCentralBearingRollingElement.emit(data)
