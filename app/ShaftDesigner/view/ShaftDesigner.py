from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStyle,
                             QVBoxLayout, QWidget, QScrollArea)
class ShaftDesigner(QMainWindow):
    """
    A class representing chart and interface to design the shaft

    This class is responsible for comunication between chart and
    other components of the application and also for implementing
    the GUI for interactive shaft design
    """
    def __init__(self, window_title):
        super().__init__()
        self._init_ui(window_title)
    
    def _init_ui(self, window_title):
        # Set window parameters
        self.setWindowTitle(window_title)
        self.resize(800,500)

        # Set layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def init_chart(self, chart):
        # Add Chart
        self._chart = chart
        self.centralWidget().layout().addWidget(self._chart)
    
    def init_sidebar(self, sections):
        # Set layout for sidebar and toggle button
        self.sidebar_section_layout  = QHBoxLayout()

        # Set sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar.setFixedWidth(200)  # Set the fixed width for the sidebar

        # Set contents of the sidebar
        for section in sections.values():
            self.sidebar_layout.addWidget(section)

        # Add a spacer item at the end of the sidebar layout - keeps the contents alignet to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebar_layout .addSpacerItem(spacer)

        # Set a scroll area for the sidebar - make the sidebar scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sidebar)
        self.scroll_area.setFixedWidth(220)  # Slightly larger to accommodate scrollbar

        # Set sidebar toggle button
        self.toggle_button_layout = QVBoxLayout()

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)  # Example icon
        self.toggle_button = QPushButton(icon, '')
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                border: none;
            }                               
        """)
        self.toggle_button.setFixedWidth(50)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button_layout.addWidget(self.toggle_button)
        self.toggle_button_layout.addStretch(1)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(self.toggle_button_layout)

    def toggle_sidebar(self):
        self.scroll_area.setVisible(not self.scroll_area.isVisible())
