from ast import literal_eval
from abc import ABCMeta, abstractmethod
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton, 
    QLabel,
    QLineEdit,
    QComboBox,
)

class MainWindow(QMainWindow):
    updatedShaftDataSignal = pyqtSignal(dict)
    updatedSupportBearingsSignal = pyqtSignal()
    updatedCycloBearingsSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        # Set signals 
        self.signals = [self.updatedShaftDataSignal, self.updatedSupportBearingsSignal, self.updatedCycloBearingsSignal]
        self.initUI()
    
    def setData(self, data):
        # Set data needed for or from GUI
        self.data = data

    def initUI(self):
        self.setWindowTitle("Mechkonstruktor 2.0")

        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)
    
    def initTabs(self):

        self.tabs = []

        # Adding a regular tab
        regular_tab = Tab(self, self.check_next_tab_button)
        self.tabs.append(regular_tab)
        self.tabWidget.addTab(regular_tab, "Tab 1")

        # Adding a split tab
        split_tab = SplitTab(self, self.check_next_tab_button)
        self.tabs.append(split_tab)
        self.tabWidget.addTab(split_tab, "Tab 2")

        # Adding the rest of the tabs
        self.nextTabButton = QPushButton("Next Tab", self)
        self.nextTabButton.clicked.connect(self.next_tab)

        # Disable all tabs except the first one
        for i in range(1, self.tabWidget.count()):
            self.tabWidget.setTabEnabled(i, False)

        self.tabWidget.currentChanged.connect(self.on_tab_change)

        # Layout for the button below the tabs
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(self.nextTabButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Check if the tab is initially filled
        self.tabs[self.tabWidget.currentIndex()].check_state()
    
    def updateData(self):
        current_index = self.tabWidget.currentIndex()
        tabData = self.tabs[self.tabWidget.currentIndex()].getData()
        print(tabData)
        self.signals[current_index].emit(tabData)

    def next_tab(self):
        self.updateData()
        current_index = self.tabWidget.currentIndex()
        next_index = current_index + 1
        # Check if we're not on the last tab
        if next_index < self.tabWidget.count():
            # Check if the current tab's button has been clicked or if the next tab is already enabled
            if not self.tabWidget.isTabEnabled(next_index):
                # Enable the next tab if it's not already enabled
                self.tabWidget.setTabEnabled(next_index, True)
            # Move to the next tab
            self.tabWidget.setCurrentIndex(next_index)

    def on_tab_change(self, index):
        print("----------------Tab changed")
        # Check if the tab is initially filled
        self.tabs[index].check_state()
        
    def check_next_tab_button(self, enableButton = False, disableNextTabs = False):
        print(f"BUTTON ENABLED: {enableButton}")
        if enableButton:
            print("\"Next Tab\" button enabled")
            self.nextTabButton.setEnabled(True)
        else:
            self.nextTabButton.setEnabled(False)
        if disableNextTabs:
            self.disable_next_tabs()

    def disable_next_tabs(self):
        for i in range(self.tabWidget.currentIndex() + 1, self.tabWidget.count()):
            self.tabWidget.setTabEnabled(i, False)

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass

class TabBase(QWidget, metaclass=ABCQWidgetMeta):
    def __init__(self, window: MainWindow, on_click_callback):
        super().__init__()
        self._window = window
        self.on_click_callback = on_click_callback

        self.lineEdits = {}
        self.itemsToSelect = {}
        self.initUI()

    @abstractmethod
    def initUI(self):
        """Initialize the user interface for the tab."""
        pass
    
    def get_state(self):
        line_edit_states = [line_edit.text() for line_edit in self.findChildren(QLineEdit)]
        combo_box_states = [combo_box.currentIndex() for combo_box in self.findChildren(QComboBox)]
        return line_edit_states, combo_box_states

    def setup_state_tracking(self):
        self.line_edits = self.findChildren(QLineEdit)
        self.combo_boxes = self.findChildren(QComboBox)

        self.original_state = self.get_state()

        for line_edit in self.line_edits:
            line_edit.textChanged.connect(self.check_state)

        for combo_box in self.combo_boxes:
            combo_box.currentIndexChanged.connect(self.check_state)

    def check_state(self):
        # Check if all inputs are provided
        print(f"items to select {self.itemsToSelect}")
        all_filled = all(line_edit.text() for line_edit in self.line_edits) and \
                    all(combo_box.currentIndex() != -1 for combo_box in self.combo_boxes) and \
                    all(item is not None for item in self.itemsToSelect.values())

        current_state = self.get_state()
        state_changed = current_state != self.original_state
        if all_filled:
            if state_changed:
                self.original_state = current_state
                print(f"state_changed: {state_changed}")
                print("1.1. The state of at least on input changed but all of them are provided")
                self.on_click_callback(True, True)
            else:
                print("1.2. All inputs are provided")
                self.on_click_callback(True, False)
        else:
                print("2. At least one input is not provided")
                self.on_click_callback(False, True)
class Tab(TabBase):
    def _setTabData(self):
        attributesToAcquire = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.itemsToSelect['Materiał'] = None
        self.tabData = {key: self._window.data[key] for key in attributesToAcquire}

    def initUI(self):
        self._setTabData()

        self.setLayout(QVBoxLayout())
        
        self._viewComp1()
        self._viewComp2()
        self._viewComp3()

        self.setup_state_tracking()
    
    def getData(self):
        for attribute, lineEdit in self.lineEdits.items():
            text = lineEdit.text()
            value = literal_eval(text)
            self.tabData[attribute][0] = value
        
        return self.tabData

    def _viewComp1(self):
        comp1Layout = QVBoxLayout()
        compLabel = QLabel("Wymiary:")

        shaftLength = createDataInputRow(self, 'L','Długość wału', 'L')

        supportCoordinatesLabel = QLabel("Współrzędne podpór:")
        pinSupport = createDataInputRow(self, 'LA', 'Podpora stała A', 'L<sub>A</sub>')
        rollerSupport = createDataInputRow(self, 'LB','Podpora przesuwna B', 'L<sub>B</sub>')

        cycloDiscCoordinatesLabel = QLabel("Współrzędne tarcz obiegowych:")
        cycloDisc1 = createDataInputRow(self, 'L1', 'Tarcza obiegowa 1', 'L<sub>1</sub>')
        cycloDisc2 = createDataInputRow(self, 'L2','Tarcza obiegowa 2', 'L<sub>2</sub>')
   
        comp1Layout.addWidget(compLabel) 
        comp1Layout.addLayout(shaftLength)
        comp1Layout.addWidget(supportCoordinatesLabel)
        comp1Layout.addLayout(pinSupport)
        comp1Layout.addLayout(rollerSupport)
        comp1Layout.addWidget(cycloDiscCoordinatesLabel)
        comp1Layout.addLayout(cycloDisc1)
        comp1Layout.addLayout(cycloDisc2)
        
        self.layout().addLayout(comp1Layout)

    def _viewComp2(self):
        comp2Layout = QVBoxLayout()
        compLabel = QLabel("Współczynnik bezpieczeństwa:")
        fos = createDataInputRow(self, 'xz', "", "x<sub>z</sub> = ")

        comp2Layout.addWidget(compLabel)
        comp2Layout.addLayout(fos)

        self.layout().addLayout(comp2Layout)

    def _viewComp3(self):
        self.comp2Layout = QVBoxLayout()
        compLabel = QLabel("Materiał")
        
        self.SelectMaterialBtn = QPushButton("Wybierz Materiał")

        self.comp2Layout.addWidget(compLabel)
        self.comp2Layout.addWidget(self.SelectMaterialBtn)

        self.layout().addLayout(self.comp2Layout)
    
    def updateViewedMaterial(self, itemData):
        self.SelectMaterialBtn.setText(itemData['Materiał'][0])
        self.tabData['Materiał'] = itemData
        self.itemsToSelect['Materiał'] = True
        self.check_state()

class SplitTab(TabBase):
   def initUI(self):
        super().initUI()  # Initialize the UI from the parent class

        # Retrieve the layout set by the parent class
        self.setLayout(QVBoxLayout())

        # Create the left and right sections as QVBoxLayouts
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Add widgets to the left layout
        left_layout.addWidget(QLineEdit("text"))

        # Add widgets to the right layout
        right_layout.addWidget(QLineEdit("text"))

        # Create a horizontal layout to hold the two sections
        h_layout = QHBoxLayout()
        h_layout.addLayout(left_layout)
        h_layout.addLayout(right_layout)

        # Add the horizontal layout to the main layout
        self.layout().addLayout(h_layout)

        self.setup_state_tracking()

def createDataInputRow(tab: TabBase, attribute, description, symbol):
    # Set Layout of the row
    layout = QHBoxLayout()
    # Create description label
    Descriptionlabel = QLabel(description)
    # Create symbol label
    SymbolLabel = QLabel(f'{symbol} = ')
    # Create LineEdit
    lineEdit = QLineEdit()
    # Fill in the Line Edit if attribute already has a value
    value = tab.tabData[attribute][0]
    if value is not None:
        lineEdit.setText(f'{value}')
    # Set input validation for LineEdit
    regex = QRegularExpression("[0-9]+")
    inputValidator = QRegularExpressionValidator(regex, lineEdit)
    lineEdit.setValidator(inputValidator)
    # Create units label
    unitsLabel = QLabel(tab.tabData[attribute][-1])

    layout.addWidget(Descriptionlabel)
    layout.addWidget(SymbolLabel)
    layout.addWidget(lineEdit)
    layout.addWidget(unitsLabel)
    # Save the LineEdit
    tab.lineEdits[attribute] = lineEdit

    return layout