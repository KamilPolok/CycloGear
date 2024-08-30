from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget

from ...common.widgets.DataButton import DataButton
from ...common.widgets.Section import Section
from ...common.widgets.ITrackedTab import ITrackedTab
from ...common.pyqt_helpers import createDataDisplayRow, createDataInputRow, createHeader

class BearingsTab(ITrackedTab):
    sectionInputsProvided = pyqtSignal(str, bool, bool)

    def _init_selector(self):
        selector_layout = QHBoxLayout()

        layout_selector_label = createHeader('Miejsce osadzenia łożyska:', bold=True)

        self.layout_selector = QComboBox()
        self.layout_selector.setFixedWidth(150)
        self.layout_selector.setEditable(True)
        line_edit = self.layout_selector.lineEdit()
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit.setReadOnly(True)
 
        self.layout_selector.addItems(["Podpora przesuwna A", "Podpora stała B", "Mimośrody"])
        self.layout_selector.currentIndexChanged.connect(self._on_change_section)

        selector_layout.addWidget(layout_selector_label, alignment=Qt.AlignmentFlag.AlignLeft)
        selector_layout.addWidget(self.layout_selector, alignment=Qt.AlignmentFlag.AlignLeft)
        selector_layout.addStretch(1)

        self.main_layout.addLayout(selector_layout)

    def _init_sections(self):
        self.stacked_sections = QStackedWidget()

        for section_name in self._items['Bearings']:
            container = self._init_bearings_section(section_name)
            self.stacked_sections.addWidget(container)

        self.main_layout.addWidget(self.stacked_sections)

    def _init_bearings_section(self, section_name):
        """
        Create and layout the UI components for single bearings section.
        """
        section_layout = QVBoxLayout()

        # Set content container
        container = QWidget()
        container.setLayout(section_layout)

        # Set section for displaying outputs and inputs
        section = Section(self, section_name, self.sectionInputsProvided.emit)

        # Set data display and input rows
        section.addWidget(createDataDisplayRow(self._outputs['Bearings'][section_name]['dip'], 'd<sub>min</sub>', 'Minimalna średnica wewnętrzna łożyska', decimalPrecision=2))
        section.addWidget(createDataInputRow(self._inputs['Bearings'][section_name]['Lh'], 'L<sub>h</sub>', 'Trwałość godzinowa łożyska', decimalPrecision=0))
        section.addWidget(createDataInputRow(self._inputs['Bearings'][section_name]['fd'], 'f<sub>d</sub>', 'Współczynnik zależny od zmiennych obciążeń dynamicznych łożyska', decimalPrecision=2))
        section.addWidget(createDataInputRow(self._inputs['Bearings'][section_name]['ft'], 'f<sub>t</sub>', 'Współczynnik zależny od temperatury pracy łożyska', decimalPrecision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = createHeader('Łożysko:', bold=True)

        select_bearing_button = DataButton('Wybierz Łożysko')
        self._items['Bearings'][section_name]['data'] = select_bearing_button

        button_layout.addWidget(button_label)
        button_layout.addWidget(select_bearing_button)

        section_layout.addWidget(section)
        section_layout.addWidget(createDataDisplayRow(self._inputs['Bearings'][section_name]['C'], 'C', 'Wymagana nośność łożyska', decimalPrecision=2))
        section_layout.addLayout(button_layout)
        section_layout.addStretch()

        return container

    def _on_change_section(self, index):
        """
        Perform actions on section change.
        """
        self.stacked_sections.setCurrentIndex(index)
        
        # Call method onActivated for every subsection in activated section
        [section.onActivated() for section in self.stacked_sections.currentWidget().findChildren(Section)]
    
    def enable_select_bearing_button(self, section_name, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.

        Args:
            section_name (str): Specifies the bearing location.
            enable_button (bool): Specifies whether the button should be enabled or disabled
            delete_choice (bool): Specifies whether the button should be reseted (clearing its id and data)
        """
        self._items['Bearings'][section_name]['data'].setEnabled(enable_button)

        if delete_choice:
            self._items['Bearings'][section_name]['data'].clear()
    
    def update_selected_bearing(self, section_name, item_data):
        """
        Update the displayed code for the selected bearing.

        Args:
            section_name (str): Specifies the bearing location.
            item_data (dict): Data of the selected item.
        """
        self._items['Bearings'][section_name]['data'].setData(item_data)
    
    def initUI(self, items, inputs, outputs):
        """
        Initialize the user interface.

        Args:
            items (dict): DattaButtons providing storage for selected items.
            inputs (dict): Inputs.
            outputs (dict): Outputs.
        """
        self._items = items

        self._inputs = inputs
        self._outputs = outputs

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._init_selector()
        self._init_sections()
        self.main_layout.addStretch()
        super().initUI()
