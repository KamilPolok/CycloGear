from PyQt6.QtWidgets import QVBoxLayout, QLabel, QScrollArea

from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row

class ResultsTab(ITrackedTab):
    def _view_results_section(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        self.scroll_area_layout = QVBoxLayout()
        scroll_area.setLayout(self.scroll_area_layout)

        self.scroll_area_layout.addWidget(QLabel('Ogólne:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['nwe'], 'n<sub>we</sub>', 'Prędkość obrotowa wejściowa', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Mwe'], 'M<sub>we</sub>', 'Moment obrotowy wejściowy', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Wymiary wału:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['L'], 'L', 'Długość wału wejściowego', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['LA'], 'L<sub>A</sub>', 'Współrzędna podpory przesuwnej', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['LB'], 'L<sub>B</sub>', 'Współrzędna podpory nieprzesuwnej', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['L1'], 'L<sub>1</sub>', 'Współrzędna koła obiegoweego 1', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['L2'], 'L<sub>2</sub>', 'Współrzędna koła obiegoweego 2', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['e'], 'e', 'Mimośród', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Siły i reakcje:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['F1'], 'F<sub>1</sub>', 'Siła wywierana przez koło obiegowe 1', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['F2'], 'F<sub>2</sub>', 'Siła wywierana przez koło obiegowe 2', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Ra'], 'R<sub>a</sub>', 'Reakcja podpory przesuwnej A', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Rb'], 'R<sub>b</sub>', 'Reakcja podpory stałej B', decimal_precision=2))
        self.scroll_area_layout.addWidget(QLabel('Straty mocy w łożyskach:'))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_A']['N'], 'N<sub>A</sub>', 'Podpora przesuwna A', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_B']['N'], 'N<sub>B</sub>', 'Podpora stała B', decimal_precision=2))
        self.scroll_area_layout.addLayout(create_data_display_row(self, self._outputs['Bearings']['eccentrics']['N'], 'N<sub>c</sub>', 'Koła obiegowe', decimal_precision=2))
        super().init_ui()

    def init_ui(self, outputs):
        """
        Initialize the user interface for ResultsTab.

        Args:
            outputs (dict): Outputs
        """
        self._outputs = outputs
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._view_results_section()
        super().init_ui()
