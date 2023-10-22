from PyQt6.QtWidgets import(
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechkonstruktor 2.0")
        self.setFixedSize(MAIN_WINDOW_W, MAIN_WINDOW_H)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        self._initView()

    def _initView(self):
        self.selectItemBtn = QPushButton("Wybierz łożysko")
        self.openItemsCatalogBtn = QPushButton("Otwórz katalog znormalizowanych elementów")

        self.generalLayout.addWidget(self.selectItemBtn)
        self.generalLayout.addWidget(self.openItemsCatalogBtn)