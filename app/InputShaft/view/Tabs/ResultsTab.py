from PyQt6.QtWidgets import QVBoxLayout, QLabel, QScrollArea

from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row

class ResultsTab(ITrackedTab):
    def _init_ui(self):
        """
        Initialize the user interface for ResultsTab.
        """
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        self.scroll_area_layout = QVBoxLayout()
        scroll_area.setLayout(self.scroll_area_layout)

        self.scroll_area_layout.addWidget(QLabel('Ogólne:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'nwe', self._parent.data['nwe'], 'n<sub>we</sub>', 'Prędkość obrotowa wejściowa', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'Mwe', self._parent.data['Mwe'], 'M<sub>we</sub>', 'Moment obrotowy wejściowy', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Geometria:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'L',  self._parent.data['L'], 'L', 'Długość wału wejściowego', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'LA', self._parent.data['LA'], 'L<sub>A</sub>', 'Współrzędna podpory przesuwnej', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'LB', self._parent.data['LB'], 'L<sub>B</sub>', 'Współrzędna podpory nieprzesuwnej', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'L1', self._parent.data['L1'], 'L<sub>1</sub>', 'Współrzędna koła obiegoweego 1', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'L2', self._parent.data['L2'], 'L<sub>2</sub>', 'Współrzędna koła obiegoweego 2', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'e',  self._parent.data['e'], 'e', 'Mimośród', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Siły i reakcje:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'F1',  self._parent.data['F1'], 'F<sub>1</sub>', 'Siła wywierana przez koło obiegowe 1', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'F2',  self._parent.data['F2'], 'F<sub>2</sub>', 'Siła wywierana przez koło obiegowe 2', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'Ra',  self._parent.data['Ra'], 'R<sub>a</sub>', 'Reakcja podpory przesuwnej A', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'Rb',  self._parent.data['Rb'], 'R<sub>b</sub>', 'Reakcja podpory stałej B', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Straty mocy w łożyskach:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'NA',  self._parent.data['NA'], 'N<sub>A</sub>', 'Podpora przesuwna A', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'NB',  self._parent.data['NB'], 'N<sub>B</sub>', 'Podpora stała B', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, 'Nc',  self._parent.data['Nc'], 'N<sub>c</sub>', 'Koła obiegowe', decimal_precision=2))

    def update_state(self):
        """
        Update the tab with parent data.
        """
        for attribute in self._outputs.keys():
            new_value = self._parent.data[attribute][0]
            self._outputs[attribute].setValue(new_value)
