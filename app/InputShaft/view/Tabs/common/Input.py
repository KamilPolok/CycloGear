from PyQt6.QtGui import QFocusEvent, QKeyEvent, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QLineEdit

class Input(QLineEdit):
    """Custom QLineEdit that validates input and monitors for inactivity."""

    inputConfirmedSignal = pyqtSignal(object)

    def __init__(self, parent=None, text = '', decimal_precision = 2):
        """Initializes the custom line edit with validation and inactivity monitoring.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
            text (str): The text to set. Defaults to empty string.
            decimal_precision (int): Maximum number of decimal digits for validation.
        """
        super().__init__(parent)
        self._last_text = ''

        self._validation_handler = ValidationHandler(decimal_precision)
        self.setValidator(self._validation_handler.get_validator())

        self._inactivity_monitor = InactivityMonitor()
        self._inactivity_monitor.inactivitySignal.connect(self._emit_input_confirmed_signal)
        self.textEdited.connect(self._inactivity_monitor.reset_timer)

        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        if text:
            self.setText(text)
       
    def _emit_input_confirmed_signal(self):
        """Validates the current text and emits a signal if the text has changed."""
        validated_text = self._validation_handler.validate(self.text())
        super().setText(validated_text)
        if validated_text != self._last_text:
            self._last_text = validated_text
            self.inputConfirmedSignal.emit(self)

    def setDecimalPrecision(self, max_decimal_digits):
        """Updates the maximum decimal precision of the validator.

        Args:
            max_decimal_digits (int): New maximum number of decimal digits.
        """
        self._validation_handler.update_validator(max_decimal_digits)
        self.setValidator(self._validation_handler.get_validator())
        self.setText(self.text())

    def setText(self, text):
        """Sets the text after validation.

        Args:
            text (str): The text to set.
        """
        validated_text = self._validation_handler.validate(text)
        self._last_text = validated_text
        super().setText(validated_text)

    def clear(self):
        """Clears the current text and resets the last text record."""
        self._last_text = ''
        super().clear()

    def keyPressEvent(self, event: QKeyEvent):
        """Handles key press events, validating and confirming input on Enter or Return.

        Args:
            event (QKeyEvent): The key event.
        """
        super().keyPressEvent(event)
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            self._inactivity_monitor.stop_timer()
            self._emit_input_confirmed_signal()

    def focusOutEvent(self, event: QFocusEvent):
        """Handles focus out events, validating and confirming input when focus is lost.

        Args:
            event (QFocusEvent): The focus event.
        """
        super().focusOutEvent(event)
        self._inactivity_monitor.stop_timer()
        self._emit_input_confirmed_signal()

class InactivityMonitor(QObject):
    """Monitors inactivity and emits a signal after a specified timeout interval."""
    
    inactivitySignal = pyqtSignal()

    def __init__(self, timeout_interval=1000):
        """Initializes the monitor with a specified timeout interval.

        Args:
            timeout_interval (int): The inactivity timeout interval in milliseconds.
        """
        super().__init__()
        self._timeout_interval = timeout_interval
        self._timer = QTimer()
        self._timer.setInterval(self._timeout_interval)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.inactivitySignal.emit)
        QApplication.instance().aboutToQuit.connect(self.handleAboutToQuit)
    
    def stop_timer(self):
        """Stops the inactivity timer if it is active."""
        if self._timer.isActive():
            self._timer.stop()

    def reset_timer(self):
        """Resets the inactivity timer, restarting it from the beginning."""
        self.stop_timer()
        self._timer.start()
    
    def handleAboutToQuit(self):
        self.stop_timer()

class ValidationHandler:
    """Handles input validation based on specified rules for decimal digits."""
    
    def __init__(self, max_decimal_digits):
        """Initializes the validator with a maximum number of decimal digits.

        Args:
            max_decimal_digits (int): Maximum allowed decimal digits in the input.
        """
        self.update_validator(max_decimal_digits)

    def update_validator(self, max_decimal_digits):
        """Updates the validation pattern based on the maximum decimal digits.

        Args:
            max_decimal_digits (int): New maximum number of decimal digits.
        """
        self._max_decimal_digits = max_decimal_digits
      
        # Base pattern for the integer part
        integer_pattern = "(0|[1-9][0-9]{0,6})"
    
        # Optional decimal part pattern, included only if max_decimal_digits > 0
        decimal_pattern = f"(\\.[0-9]{{1,{max_decimal_digits}}})" if max_decimal_digits > 0 else ""
    
        # Combine patterns. Make decimal part optional in regex if max_decimal_digits > 0
        pattern = f"^{integer_pattern}{decimal_pattern}?$" if max_decimal_digits > 0 else f"^{integer_pattern}$"

        self.validator = QRegularExpressionValidator(QRegularExpression(pattern))
    
    def get_validator(self):
        """Returns the current validator."""
        return self.validator

    def validate(self, text):
        """Validates the input text, ensuring it's a positive number formatted to the specified precision.

        Args:
            text (str): The input text to validate.

        Returns:
            str: The validated text formatted to the specified precision, or an empty string if invalid.
        """
        try:
            value = float(text)
            if value <= 0:
                res = ''
            else:
                rounded_value = round(value, self._max_decimal_digits)
                res = f'{rounded_value:.{self._max_decimal_digits}f}'
        except (ValueError, TypeError):
            res = ''
        
        return res
