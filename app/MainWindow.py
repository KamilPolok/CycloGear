from ast import literal_eval
from abc import ABCMeta, abstractmethod
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton, 
    QLabel,
    QLineEdit,
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
        self.tabWidget.addTab(regular_tab, "Założenia wstępne")
        # Adding a split tab
        split_tab = SplitTab(self, self.check_next_tab_button)
        self.tabs.append(split_tab)
        self.tabWidget.addTab(split_tab, "Dobór łożysk")
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
        # Check if the tab is initially filled
        self.tabs[index].check_state()
        self.tabs[index].updateTab()
        
    def check_next_tab_button(self, enableButton = False, disableNextTabs = False):
        if enableButton:
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
        # Set the inputs and labels dicts to enable tracking of them 
        self.lineEdits = {}
        self.itemsToSelect = {}
        
        self.valueLabels = {}
        # init UI
        self.initUI()
        self.setup_state_tracking()

    @abstractmethod
    def initUI(self):
        """Initialize the user interface for the tab."""
        pass
    
    def updateTab(self):
        pass
    
    def get_state(self):
        # get all inputs states
        inputs_states =  [line_edit.text() for line_edit in self.line_edits]
        inputs_states +=  [item for item in self.itemsToSelect.values()]
        # Check if any of the inputs was not provided
        if ('' in inputs_states):
            # ...if yes, return None
            return None
            # ...if no, return them
        else:
            return inputs_states

    def setup_state_tracking(self):
        # Get all the inputs to track if they are provided
        self.line_edits = self.findChildren(QLineEdit)
        # Set the original state
        self.original_state = self.get_state()
        # Connect the inputs with function that will get their state if it will change
        for line_edit in self.line_edits:
            line_edit.textChanged.connect(self.check_state)

    def check_state(self):
        # This function gets invoked when the state of a input was changed
        # ...and on switching to another tab
         
        # Get current state of inputs
        state_changed = False
        current_state = self.get_state()
        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        if all_filled:
            # Check if originally all inputs were provided
            if self.original_state:
                # ...if yes, check if the state changed
                state_changed = current_state != self.original_state
            # Set the current state as original state
            self.original_state = current_state

            if state_changed:
                # All inputs were provided but at least one of them was changed 
                self.on_click_callback(True, True)
            else:
                # All inputs were provided no one of them was changed
                self.on_click_callback(True, False)
        else:
            # At least one input is not provided
            self.on_click_callback(False, True)
class Tab(TabBase):
    updatedDataSignal = pyqtSignal(dict)

    def _setTabData(self):
        attributesToAcquire = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.tabData = {key: self._window.data[key] for key in attributesToAcquire}

        self.itemsToSelect['Materiał'] = ''

    def initUI(self):
        self._setTabData()

        self.setLayout(QVBoxLayout())
        
        self._viewComp1()
        self._viewComp2()
        self._viewComp3()

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
        fos = createDataInputRow(self, 'xz', "", "x<sub>z</sub>")

        comp2Layout.addWidget(compLabel)
        comp2Layout.addLayout(fos)

        self.layout().addLayout(comp2Layout)

    def _viewComp3(self):
        componentLayout = QHBoxLayout()
        componentLabel = QLabel("Materiał:")

        self.SelectMaterialBtn = QPushButton("Wybierz Materiał")

        componentLayout.addWidget(componentLabel)
        componentLayout.addWidget(self.SelectMaterialBtn)

        self.layout().addLayout(componentLayout)
    
    def updateViewedMaterial(self, itemData):
        print(itemData)
        self.SelectMaterialBtn.setText(str(itemData['Materiał'][0]))
        self.tabData['Materiał'] = itemData
        self.itemsToSelect['Materiał'] = str(itemData['Materiał'][0])
        self.check_state()
    
    def getData(self):
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

    def __init__(self, window: MainWindow, on_click_callback):
        super().__init__(window, on_click_callback)
        self.setup_layouts_state_tracking()

    def _setTabData(self):
        attributesToAcquire = ['Lh1', 'fd1', 'ft1', 'Łożyska1']
        attributesToAcquire += ['Lh2', 'fd2', 'ft2', 'Łożyska2']
        self.tabData = {key: self._window.data[key] for key in attributesToAcquire}

        self.itemsToSelect['Łożyska1'] = ''
        self.itemsToSelect['Łożyska2'] = ''

    def initUI(self):
        self._setTabData()

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

    def viewSection1(self):
        sectionLabel = QLabel("Łożyska osadzone na wale:")
        ds = createDataDisplayRow(self, 'ds','Obliczona średnica wału', 'd<sub>s</sub>')
        lh = createDataInputRow(self, 'Lh1', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>')
        fd = createDataInputRow(self, 'ft1', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = createDataInputRow(self, 'fd1', 'Współczynnik zależny od temperatury pracy łożyska', 'f<sub>t</sub>')
        # Set button for selecting first type of bearing
        btnLayout = QHBoxLayout()
        btnLabel = QLabel("Łożysko:")

        self.SelectBearingBtn1 = QPushButton("Wybierz łożysko")
        self.SelectBearingBtn1.setEnabled(False)
        self.SelectBearingBtn1.clicked.connect(self.updateBearings1Data)

        btnLayout.addWidget(btnLabel)
        btnLayout.addWidget(self.SelectBearingBtn1)

        self.left_layout.addWidget(sectionLabel)
        self.left_layout.addLayout(ds)
        self.left_layout.addLayout(lh)
        self.left_layout.addLayout(fd)
        self.left_layout.addLayout(ft)
        self.left_layout.addLayout(btnLayout)

    def viewSection2(self):
        sectionLabel = QLabel("Łożyska osadzone na wykorbieniach:")
        de = createDataDisplayRow(self, 'de','Obliczona średnica wykorbienia', 'd<sub>e</sub>')
        lh = createDataInputRow(self, 'Lh2', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>')
        fd = createDataInputRow(self, 'ft2', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = createDataInputRow(self, 'fd2', 'Współczynnik zależny od temperatury pracy łozyska', 'f<sub>t</sub>')
        # Set button for selecting second type of bearing
        btnLayout = QHBoxLayout()
        btnLabel = QLabel("Łożysko:")

        self.SelectBearingBtn2 = QPushButton("Wybierz łożysko")
        self.SelectBearingBtn2.setEnabled(False)
        self.SelectBearingBtn2.clicked.connect(self.updateBearings2Data)

        btnLayout.addWidget(btnLabel)
        btnLayout.addWidget(self.SelectBearingBtn2)

        self.right_layout.addWidget(sectionLabel)
        self.right_layout.addLayout(de)
        self.right_layout.addLayout(lh)
        self.right_layout.addLayout(fd)
        self.right_layout.addLayout(ft)
        self.right_layout.addLayout(btnLayout)


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
        # This function checks the state of the left layout in the tab

        # Get current state of inputs
        state_changed = False
        current_state = self.get_layout_state(self.left_line_edits)
        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        if all_filled:
            # Check if originally all inputs were provided
            if self.left_layout_original_state:
                # ...if yes, check if the state changed
                state_changed = current_state != self.left_layout_original_state
            # Set the current state as original state
            self.left_layout_original_state = current_state

            if state_changed:
                # All inputs were provided but at least one of them was changed
                self.SelectBearingBtn1.setEnabled(True)
                self.SelectBearingBtn1.setText("Wybierz Łożysko")
                self.itemsToSelect['Łożyska1'] = ''
                self.check_state()
            else:
                # All inputs were provided no one of them was changed
                self.SelectBearingBtn1.setEnabled(True)
        else:
            # At least one input is not provided
            self.SelectBearingBtn1.setEnabled(False)
    
    def check_right_layout_state(self):
        # This function checks the state of the right layout in the tab

        # Get current state of inputs
        state_changed = False
        current_state = self.get_layout_state(self.right_line_edits)
        # Check if all inputs are provided
        all_filled = False if current_state == None else True

        if all_filled:
            # Check if originally all inputs were provided
            if self.right_layout_original_state:
                # ...if yes, check if the state changed
                state_changed = current_state != self.right_layout_original_state
            # Set the current state as original state
            self.right_layout_original_state = current_state

            if state_changed:
                # All inputs were provided but at least one of them was changed
                self.SelectBearingBtn2.setEnabled(True)
                self.SelectBearingBtn2.setText("Wybierz Łożysko")
                self.itemsToSelect['Łożyska2'] = ''
                self.check_state()
            else:
                # All inputs were provided no one of them was changed
                self.SelectBearingBtn2.setEnabled(True)
        else:
            # At least one input is not provided
            self.SelectBearingBtn2.setEnabled(False)
    
    def updateViewedBearing1(self, itemData):
        self.SelectBearingBtn1.setText(str(itemData['kod'][0]))
        self.tabData['Łożyska1'] = itemData
        # Mark, that the item to select was selected
        self.itemsToSelect['Łożyska1'] = str(itemData['kod'][0])
        # Check if the state changed - the purpose here is to confirm
        # ...that item to select was indeed selected
        self.check_state()

    def updateViewedBearing2(self, itemData):
        self.SelectBearingBtn2.setText(str(itemData['kod'][0]))
        self.tabData['Łożyska2'] = itemData
        # Mark, that the item to select was selected
        self.itemsToSelect['Łożyska2'] = str(itemData['kod'][0])
        # Check if the state changed - the purpose here is to confirm
        # ...that item to select was indeed selected
        self.check_state()
    
    def getData(self):
        for attribute, lineEdit in self.lineEdits.items():
            text = lineEdit.text()
            value = None if text == "" else literal_eval(text)
            self.tabData[attribute][0] = value
        
        return self.tabData
    
    def updateBearings1Data(self):
        tabData = self.getData()
        self.updatedBearings1DataSignal.emit(tabData)

    def updateBearings2Data(self):
        tabData = self.getData()
        self.updatedBearings2DataSignal.emit(tabData)

    def updateData(self):
        tabData = self.getData()
        self.updatedDataSignal.emit(tabData)
    
    def updateTab(self):
        for key, value in self.valueLabels.items():
            if value != self._window.data[key][0]:
                value = self._window.data[key][0]
                self.valueLabels[key].setText(f'{value:.2f}')

def createDataInputRow(tab: TabBase, attribute, description, symbol):
    # Set Layout of the row
    layout = QHBoxLayout()
    # Create description label
    descriptionlabel = QLabel()
    descriptionlabel = QLabel(description)
    descriptionlabel.setFixedWidth(150)
    descriptionlabel.setWordWrap(True) 
    # Create symbol label
    symbolLabel = QLabel(f'{symbol} = ')
    symbolLabel.setFixedWidth(20)
    # Create LineEdit
    lineEdit = QLineEdit()
    lineEdit.setFixedWidth(80)
    # Fill in the Line Edit if attribute already has a value
    value = tab.tabData[attribute][0]
    if value is not None:
        lineEdit.setText(f'{value}')
    # Set input validation for LineEdit
    regex = QRegularExpression("^(0|[1-9][0-9]{0,6})(\.[0-9]{1,4})?$")
    inputValidator = QRegularExpressionValidator(regex, lineEdit)
    lineEdit.setValidator(inputValidator)
    # Create units label
    unitsLabel = QLabel(tab.tabData[attribute][-1])
    unitsLabel.setFixedWidth(20)

    layout.addWidget(descriptionlabel)
    layout.addWidget(symbolLabel)
    layout.addWidget(lineEdit)
    layout.addWidget(unitsLabel)
    # Save the LineEdit
    tab.lineEdits[attribute] = lineEdit

    return layout

def createDataDisplayRow(tab: TabBase, attribute, description, symbol):
    # Set Layout of the row
    layout = QHBoxLayout()
    # Create description label
    descriptionlabel = QLabel(description)
    descriptionlabel.setFixedWidth(150)
    descriptionlabel.setWordWrap(True)
    # Create symbol label
    symbolLabel = QLabel(symbol)
    symbolLabel = QLabel(f'{symbol} = ')
    symbolLabel.setFixedWidth(20)
    # Create label that holds the value of the attribute
    valueLabel = QLineEdit(tab._window.data[attribute][0] if tab._window.data[attribute][0] is not None else '')
    valueLabel.setReadOnly(True)
    valueLabel.setFixedWidth(80)
    # Create units label
    unitsLabel = QLabel(tab._window.data[attribute][-1])
    unitsLabel.setFixedWidth(20)
    
    layout.addWidget(descriptionlabel)
    layout.addWidget(symbolLabel)
    layout.addWidget(valueLabel)
    layout.addWidget(unitsLabel)
    # Save the label
    tab.valueLabels[attribute] = valueLabel

    return layout
