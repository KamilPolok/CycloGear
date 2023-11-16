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
    def __init__(self):
        super().__init__()
        # Set signals 
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

    def next_tab(self):
        current_index = self.tabWidget.currentIndex()
        next_index = current_index + 1
        # Check if we're not on the last tab
        if next_index < self.tabWidget.count():
            # Check if the current tab's button has been clicked or if the next tab is already enabled
            if not self.tabWidget.isTabEnabled(next_index):
                # Enable the next tab if it's not already enabled
                self.tabWidget.setTabEnabled(next_index, True)
            # Move to the next tab
            self.tabs[current_index].updateData()
            self.tabWidget.setCurrentIndex(next_index)

    def on_tab_change(self, index):
        print("----------------Tab changed")
        # Check if the tab is initially filled
        self.tabs[index].check_state()
        self.tabs[index].updateTab()
        
    def check_next_tab_button(self, enableButton = False, disableNextTabs = False):
        # print(f"BUTTON ENABLED: {enableButton}")
        if enableButton:
            # print("\"Next Tab\" button enabled")
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
        
        self.valueLabels = {}

        self.initUI()

    @abstractmethod
    def initUI(self):
        """Initialize the user interface for the tab."""
        pass
    
    def updateTab(self):
        pass
    
    def get_state(self):
        inputs_states =  [line_edit.text() for line_edit in self.line_edits]
        inputs_states += [combo_box.currentIndex() for combo_box in self.combo_boxes]

        if ('' in inputs_states or -1 in inputs_states) or not all(item is not None for item in self.itemsToSelect.values()):
            return None
        else:
            return inputs_states

    def setup_state_tracking(self):
        self.line_edits = self.findChildren(QLineEdit)
        self.combo_boxes = self.findChildren(QComboBox)

        self.original_state = self.get_state()

        for line_edit in self.line_edits:
            line_edit.textChanged.connect(self.check_state)

        for combo_box in self.combo_boxes:
            combo_box.currentIndexChanged.connect(self.check_state)

    def check_state(self):
        state_changed = False
        current_state = self.get_state()

        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        print(f"currentstate: {current_state}")
        if all_filled:
            current_state = self.get_state()
            if self.original_state:
                state_changed = current_state != self.original_state
            self.original_state = current_state

            if state_changed:
                # print(f"state_changed: {state_changed}")
                # print("1.1. The state of at least on input changed but all of them are provided")
                self.on_click_callback(True, True)
            else:
                # print("1.2. All inputs are provided")
                self.on_click_callback(True, False)
        else:
            # print("2. At least one input is not provided")
            self.on_click_callback(False, True)
class Tab(TabBase):
    updatedDataSignal = pyqtSignal(dict)

    def _setTabData(self):
        attributesToAcquire = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.tabData = {key: self._window.data[key] for key in attributesToAcquire}

        self.itemsToSelect['Materiał'] = None

    def initUI(self):
        self._setTabData()

        self.setLayout(QVBoxLayout())
        
        self._viewComp1()
        self._viewComp2()
        self._viewComp3()

        self.setup_state_tracking()

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
    
    def getData(self):
        print(f"Line edits: {self.lineEdits}")
        for attribute, lineEdit in self.lineEdits.items():
            text = lineEdit.text()
            value = literal_eval(text)
            self.tabData[attribute][0] = value
        
        return self.tabData
    
    def updateData(self):
        tabData = self.getData()
        self.updatedDataSignal.emit(tabData)

class SplitTab(TabBase):
    updatedDataSignal = pyqtSignal(dict)
    updatedBearings1DataSignal = pyqtSignal(dict)
    updatedBearings2DataSignal = pyqtSignal(dict)

    def _setTabData(self):
            attributesToAcquire = ['Lh1', 'fd1', 'ft1', 'Łożyska1']
            attributesToAcquire += ['Lh2', 'fd2', 'ft2', 'Łożyska2']
            self.tabData = {key: self._window.data[key] for key in attributesToAcquire}
            print(self.tabData)

            self.itemsToSelect['Łożyska1'] = None
            self.itemsToSelect['Łożyska2'] = None

    def initUI(self):
        super().initUI()  # Initialize the UI from the parent class

        self._setTabData()

        # Retrieve the layout set by the parent class
        self.setLayout(QVBoxLayout())

        # Create the left and right sections as QVBoxLayouts
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Create a horizontal layout to hold the two sections
        h_layout = QHBoxLayout()
        h_layout.addLayout(self.left_layout)
        h_layout.addLayout(self.right_layout)

        # Add the horizontal layout to the main layout
        self.layout().addLayout(h_layout)

        self.viewSection1()
        self.viewSection2()

        self.setup_state_tracking()
        self.setup_layouts_state_tracking()

    def viewSection1(self):
        ds = createDataDisplayRow(self, 'ds','Średnica wału', 'd<sub>s</sub>')
        lh = createDataInputRow(self, 'Lh1', 'trwałość godzinowa łożyska', 'f<sub>d</sub>')
        fd = createDataInputRow(self, 'ft1', 'współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = createDataInputRow(self, 'fd1', 'współczynnik zależny od temperatury pracy łozyska', 'f<sub>t</sub>')
        # Set 
        self.SelectBearingBtn1 = QPushButton("Wybierz łożysko")
        self.SelectBearingBtn1.setEnabled(False)
        self.SelectBearingBtn1.clicked.connect(self.updateBearings1Data)

        self.left_layout.addLayout(ds)
        self.left_layout.addLayout(lh)
        self.left_layout.addLayout(fd)
        self.left_layout.addLayout(ft)
        self.left_layout.addWidget(self.SelectBearingBtn1)

    def setup_layouts_state_tracking(self):
        self.left_line_edits =  [le for le in self.line_edits if self.is_widget_in_layout(le, self.left_layout)]
        self.right_line_edits =  [le for le in self.line_edits if self.is_widget_in_layout(le, self.right_layout)]

        self.left_layout_original_state = self.get_layout_state(self.left_line_edits)
        self.right_layout_original_state = self.get_layout_state(self.right_line_edits)

        for line_edit in self.left_line_edits:
            line_edit.textChanged.connect(self.check_left_layout_state)

        for line_edit in self.right_line_edits:
            line_edit.textChanged.connect(self.check_right_layout_state)

    def get_layout_state(self, line_edits):
        layout_input_states = [line_edit.text() for line_edit in line_edits]
        print(layout_input_states)
        if '' in layout_input_states:
            return None
        else:
            return layout_input_states

    def is_widget_in_layout(self, widget, layout):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == widget:
                    return True
                elif item.layout() and self.is_widget_in_layout(widget, item.layout()):
                    return True
            return False
    
    def check_left_layout_state(self):
        print("Checking left layout state")
        state_changed = False
        current_state = self.get_layout_state(self.left_line_edits)
        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        if all_filled:
            current_state = self.get_state()
            if self.original_state:
                state_changed = current_state != self.original_state
            self.original_state = current_state

            if state_changed:
                self.left_layout_original_state = current_state
                print(f"state_changed: {state_changed}")
                print("1.1. The state of at least on input changed but all of them are provided")
                self.SelectBearingBtn1.setEnabled(False)
            else:
                print("1.2. All inputs are provided")
                self.SelectBearingBtn1.setEnabled(True)
        else:
                print("2. At least one input is not provided")
                self.SelectBearingBtn1.setEnabled(False)
    
    def check_right_layout_state(self):
        print("Checking right layout state")
        state_changed = False
        current_state = self.get_layout_state(self.right_line_edits)
        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        if all_filled:
            current_state = self.get_state()
            if self.original_state:
                state_changed = current_state != self.original_state
            self.original_state = current_state

            if state_changed:
                self.right_layout_original_state = current_state
                print(f"state_changed: {state_changed}")
                print("1.1. The state of at least on input changed but all of them are provided")
                self.SelectBearingBtn2.setEnabled(False)
            else:
                print("1.2. All inputs are provided")
                self.SelectBearingBtn2.setEnabled(True)
        else:
                print("2. At least one input is not provided")
                self.SelectBearingBtn2.setEnabled(False)
    
    def viewSection2(self):
        de = createDataDisplayRow(self, 'de','Średnica wału', 'd<sub>s</sub>')
        lh = createDataInputRow(self, 'Lh2', 'trwałość godzinowa łożyska', 'f<sub>d</sub>')
        fd = createDataInputRow(self, 'ft2', 'współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = createDataInputRow(self, 'fd2', 'współczynnik zależny od temperatury pracy łozyska', 'f<sub>t</sub>')

        # Set 
        self.SelectBearingBtn2 = QPushButton("Wybierz łożysko")
        self.SelectBearingBtn2.setEnabled(False)
        self.SelectBearingBtn2.clicked.connect(self.updateBearings2Data)


        self.right_layout.addLayout(de)
        self.right_layout.addLayout(lh)
        self.right_layout.addLayout(fd)
        self.right_layout.addLayout(ft)
        self.right_layout.addWidget(self.SelectBearingBtn2)
    
    def updateViewedBearing1(self, itemData):
        self.SelectBearingBtn1.setText(itemData['kod'][0])
        self.tabData['Łożyska1'] = itemData
        self.itemsToSelect['Łożyska1'] = True
        self.check_state()

    def updateViewedBearing2(self, itemData):
        self.SelectBearingBtn2.setText(itemData['kod'][0])
        self.tabData['Łożyska2'] = itemData
        self.itemsToSelect['Łożyska2'] = True
        self.check_state()
    
    def getData(self):
        for idx, lineedit in self.lineEdits.items():
            print(lineedit.text())

        for attribute, lineEdit in self.lineEdits.items():
            text = lineEdit.text()
            value = None if text == "" else literal_eval(text)
            self.tabData[attribute][0] = value
        
        return self.tabData
    
    def updateBearings1Data(self):
        tabData = self.getData()
        print(tabData)
        self.updatedBearings1DataSignal.emit(tabData)

    def updateBearings2Data(self):
        tabData = self.getData()
        self.updatedBearings2DataSignal.emit(tabData)

    def updateData(self):
        tabData = self.getData()
        self.updatedDataSignal.emit(tabData)
    
    def updateTab(self):
        print("LABELS")
        for key, value in self.valueLabels.items():
            value = self._window.data[key][0]
            self.valueLabels[key].setText(f'{value}')
        print(self.valueLabels)

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

def createDataDisplayRow(tab: TabBase, attribute, description, symbol):
    layout = QHBoxLayout()
    descriptionlabel = QLabel(description)
    attributeLabel = QLabel(symbol)
    valueLabel = QLabel(tab._window.data[attribute][0] if tab._window.data[attribute][0] is not None else '')
    unitsLabel = QLabel(attribute[1])
    layout.addWidget(descriptionlabel)
    layout.addWidget(attributeLabel)
    layout.addWidget(valueLabel)
    layout.addWidget(unitsLabel)

    tab.valueLabels[attribute] = valueLabel

    return layout