from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QScrollArea

from .TabIf import Tab
from .TabCommon import create_data_display_row, format_value
from .ChartView import Chart

class ResultsTab(Tab):
    def init_ui(self):
        """
        Initialize the user interface for ResultsTab.
        """
        self.setLayout(QVBoxLayout())
        
        self._subtab_widget = QTabWidget(self)
        self.layout().addWidget(self._subtab_widget)

        self.add_data_subtab()
        self.add_results_subtab()
        self.add_chart_subtab()

    def add_data_subtab(self):
        """
        Add a subtab for displaying data.
        """
        subtab = QScrollArea()
        subtab.setWidgetResizable(True)
        self._subtab_widget.addTab(subtab, 'Dane')

        content_widget = QWidget()
        self.data_subtab_layout = QVBoxLayout(content_widget)
        subtab.setWidget(content_widget)

        generalDataLabel = QLabel('Ogólne:')
        nwe = create_data_display_row(self, 'nwe', self._window.data['nwe'], 'n<sub>we</sub>', 'Prędkość obrotowa wejściowa')
        mwe = create_data_display_row(self, 'Mwe', self._window.data['Mwe'], 'M<sub>we</sub>', 'Moment obrotowy wejściowy')
        dimensionsLabel = QLabel('Wymiary:')
        l = create_data_display_row(self, 'L',  self._window.data['L'], 'L', 'Długość wału',)
        e = create_data_display_row(self, 'e',  self._window.data['e'], 'e', 'Mimośród')
        supportCoordinatesLabel = QLabel('Współrzędne podpór:')
        pinSupport = create_data_display_row(self, 'LA', self._window.data['LA'], 'L<sub>A</sub>', 'Podpora stała A',)
        rollerSupport = create_data_display_row(self, 'LB', self._window.data['LB'], 'L<sub>B</sub>', 'Podpora przesuwna B')
        cycloDiscCoordinatesLabel = QLabel('Współrzędne kół obiegowych:')
        cycloDisc1 = create_data_display_row(self, 'L1', self._window.data['L1'], 'L<sub>1</sub>', 'Tarcza obiegowa 1')
        cycloDisc2 = create_data_display_row(self, 'L2', self._window.data['L2'], 'L<sub>2</sub>', 'Tarcza obiegowa 2')
        materialsLabel = QLabel('Materiał:')
        
        self.data_subtab_layout.addWidget(generalDataLabel)
        self.data_subtab_layout.addLayout(nwe)
        self.data_subtab_layout.addLayout(mwe)
        self.data_subtab_layout.addWidget(dimensionsLabel)
        self.data_subtab_layout.addLayout(l)
        self.data_subtab_layout.addLayout(e)
        self.data_subtab_layout.addWidget(supportCoordinatesLabel)
        self.data_subtab_layout.addLayout(pinSupport)
        self.data_subtab_layout.addLayout(rollerSupport)
        self.data_subtab_layout.addWidget(cycloDiscCoordinatesLabel)
        self.data_subtab_layout.addLayout(cycloDisc1)
        self.data_subtab_layout.addLayout(cycloDisc2)
        self.data_subtab_layout.addWidget(materialsLabel)

    def add_results_subtab(self):
        """
        Add a subtab for displaying results.
        """
        subtab = QScrollArea()
        subtab.setWidgetResizable(True)
        self._subtab_widget.addTab(subtab, 'Wyniki')

        content_widget = QWidget()
        self.results_subtab_layout = QVBoxLayout(content_widget)
        subtab.setWidget(content_widget)

        dimensionsLabel = QLabel('Wymiary')
        ds = create_data_display_row(self, 'ds',  self._window.data['ds'], 'd<sub>s</sub>', 'Średnica wału')
        de = create_data_display_row(self, 'de',  self._window.data['de'], 'd<sub>e</sub>', 'Średnica wykorbienia')

        Łożyska1 = QLabel('Łożyska')

        self.results_subtab_layout.addWidget(dimensionsLabel)
        self.results_subtab_layout.addLayout(ds)
        self.results_subtab_layout.addLayout(de)
        self.results_subtab_layout.addWidget(Łożyska1)

    def add_chart_subtab(self):
        """
        Add a subtab for displaying charts.
        """
        self._chart_tab = Chart()
        self._subtab_widget.addTab(self._chart_tab, 'Wykresy')
    
    def create_plots(self, chart_data):
        """
        Create plots in the chart tab.

        :param chart_data: Data to be used for plotting.
        """
        self._chart_tab.create_plots(chart_data)

    def update_tab(self):
        addData = True 
        for key, value in self.output_values.items():
            if key in self._window.data and value != self._window.data[key][0]:
                value = self._window.data[key][0]
                self.output_values[key].setText(format_value(value))
            elif key in self._window.data['Materiał']:
                addData = False
                value = self._window.data['Materiał'][key][0]
                self.output_values[key].setText(format_value(value))
        
        if addData:
            for key, value in self._window.data['Materiał'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.data_subtab_layout.addLayout(attribute)
            for key, value in self._window.data['Łożyska_podporowe'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.results_subtab_layout.addLayout(attribute)
            for key, value in self._window.data['Łożyska_centralne'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.results_subtab_layout.addLayout(attribute)
