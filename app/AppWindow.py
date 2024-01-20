from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        # Set window parameters
        self.setWindowTitle("CycloGear2023")
        self.resize(800,500)

        # Set layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def add_component(self, component: QWidget):
        self.main_layout.addWidget(component)
