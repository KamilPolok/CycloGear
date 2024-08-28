from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication, QPushButton, QHBoxLayout, QStyle, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtCore import QSize, Qt

class MessageDialog(QDialog):
    '''
    Custom QMessageBox designed to enhance window resizing flexibility and accommodate long titles. 
    This custom dialog is particularly useful because it prevents the truncation of lengthy titles, 
    ensuring they are fully displayed.
    ''' 
    def __init__(self, parent, title, message, icon_type):
        super().__init__(parent)

        self.title = title
        self.message = message
        self.icon_type = icon_type

        # Set window flags to keep only the title bar
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint)

        self.setWindowTitle(title)

        self.layout = QVBoxLayout(self)

        self._init_message()
        self._init_buttons()

        titleFont = QApplication.font()
        fontMetrics = QFontMetrics(titleFont)
        title_width = fontMetrics.horizontalAdvance(self.title) + 150  # Add some padding
        message_width = 200 + 32 + 20  # Text width + icon width + padding
        width = max(title_width, message_width)
        self.setMinimumWidth(width)

    def _init_message(self):
        # Message layout
        messageLayout = QHBoxLayout()
        self.layout.addLayout(messageLayout)

        # Message type icon
        self.iconLabel = QLabel()
        self.iconLabel.setFixedWidth(50)
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = self.style().standardIcon(self.icon_type)
        self.iconLabel.setPixmap(icon.pixmap(QSize(32, 32)))
        messageLayout.addWidget(self.iconLabel)

        # Message label 
        self.messageLabel = QLabel(self.message)
        self.messageLabel.setWordWrap(True)
        messageFont = QFont()
        messageFont.setPointSize(9)
        self.messageLabel.setFont(messageFont)
        messageLayout.addWidget(self.messageLabel)

    def _init_buttons(self):
        # Buttons layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(20)
        self.layout.addLayout(buttonLayout)

        if self.icon_type == QStyle.StandardPixmap.SP_MessageBoxQuestion:
            buttonLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

            # Yes Button
            self.yesButton = QPushButton("Tak")
            self.yesButton.setFixedWidth(80)
            self.yesButton.clicked.connect(self.accept)
            buttonLayout.addWidget(self.yesButton)

            # No button
            self.noButton = QPushButton("Nie")
            self.noButton.setFixedWidth(80)
            self.noButton.clicked.connect(self.reject)
            buttonLayout.addWidget(self.noButton)

            buttonLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        else:
            # OK button
            self.okButton = QPushButton("OK")
            self.okButton.clicked.connect(self.accept)
            self.okButton.setFixedWidth(80)
            buttonLayout.addWidget(self.okButton)

    @classmethod
    def critical(cls, parent, title, message):
        dialog = cls(parent, title, message, QStyle.StandardPixmap.SP_MessageBoxCritical)
        dialog.exec()

    @classmethod
    def information(cls, parent, title, message):
        dialog = cls(parent, title, message, QStyle.StandardPixmap.SP_MessageBoxInformation)
        dialog.exec()

    @classmethod
    def question(cls, parent, title, message):
        dialog = cls(parent, title, message, QStyle.StandardPixmap.SP_MessageBoxQuestion)
        return dialog.exec()

    @classmethod
    def warning(cls, parent, title, message):
        dialog = cls(parent, title, message, QStyle.StandardPixmap.SP_MessageBoxWarning)
        dialog.exec()
