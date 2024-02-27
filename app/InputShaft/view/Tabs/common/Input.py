from typing import Optional

from PyQt6.QtGui import QFocusEvent, QKeyEvent, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget

class Input(QLineEdit):
    """Custom QLineEdit that validates numeric input and monitors for inactivity."""

    inputConfirmedSignal = pyqtSignal(object)

    def __init__(self, parent: QWidget, decimal_precision: int=2):
        """
        Initialize the custom line edit with validation and inactivity monitoring.

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
       
    def _emit_input_confirmed_signal(self):
        """
        Validate the current text and emit a signal if the text has changed.
        """
        validated_text = self._validation_handler.validate(self.text())
        super().setText(validated_text)
        if validated_text != self._last_text:
            self._last_text = validated_text
            self.inputConfirmedSignal.emit(self)

    def setDecimalPrecision(self, max_decimal_digits: int):
        """
        Update the maximum decimal precision of the validator.

        Args:
            max_decimal_digits (int): New maximum number of decimal digits.
        """
        self._validation_handler.update_validator(max_decimal_digits)
        self.setValidator(self._validation_handler.get_validator())
        self.setText(self.text())

    def setText(self, text: str):
        """
        Validate and set text.

        Args:
            text (str): The text to set.
        """
        validated_text = self._validation_handler.validate(text)
        self._last_text = validated_text
        super().setText(validated_text)

    def setValue(self, value: float):
        """
        Validate and set value.

        Args:
            value (float): The value to set.
        """
        validated_text = self._validation_handler.validate_value(value)
        self._last_text = validated_text
        super().setText(validated_text)
    
    def value(self) -> Optional[float]:
        """
        Retutn value.

        Returns:
            (float | None): The value the input is holding or None if text.
        """
        text = self.text()
        return None if text == "" else float(text)

    def clear(self):
        """
        Clear the current text and reset the last text record.
        """
        self._last_text = ''
        super().clear()

    def keyPressEvent(self, event: QKeyEvent):
        """
        Handle key press events, validating and confirming input on Enter or Return.

        Args:
            event (QKeyEvent): The key event.
        """
        super().keyPressEvent(event)
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            self._inactivity_monitor.stop_timer()
            self._emit_input_confirmed_signal()

    def focusOutEvent(self, event: QFocusEvent):
        """
        Handle focus out events, validating and confirming input when focus is lost.

        Args:
            event (QFocusEvent): The focus event.
        """
        super().focusOutEvent(event)
        self._inactivity_monitor.stop_timer()
        self._emit_input_confirmed_signal()

class InactivityMonitor(QObject):
    """
    Monitor inactivity and emits a signal after a specified timeout interval.
    """
    
    inactivitySignal = pyqtSignal()

    def __init__(self, timeout_interval: int=1000):
        """
        Initialize the monitor with a specified timeout interval.

        Args:
            timeout_interval (int): The inactivity timeout interval in milliseconds.
        """
        super().__init__()
        self._timeout_interval = timeout_interval
        self._timer = QTimer()
        self._timer.setInterval(self._timeout_interval)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.inactivitySignal.emit)
        # Ensure that every timer is stopped before closing the app
        QApplication.instance().aboutToQuit.connect(self.handleAboutToQuit)
    
    def stop_timer(self):
        """
        Stop the inactivity timer if it is active.
        """
        if self._timer.isActive():
            self._timer.stop()

    def reset_timer(self):
        """
        Reset the inactivity timer, restarting it from the beginning.
        """
        self.stop_timer()
        self._timer.start()
    
    def handleAboutToQuit(self):
        self.stop_timer()

class ValidationHandler:
    """
    Handle input validation based on specified rules for decimal digits.
    """
    
    def __init__(self, max_decimal_digits: int):
        """
        Initialize the validator with a maximum number of decimal digits.

        Args:
            max_decimal_digits (int): Maximum number of decimal places permitted in the input.
        """
        self.update_validator(max_decimal_digits)

    def update_validator(self, max_decimal_digits: int):
        """
        Update the validation pattern based on the maximum decimal digits.

        Args:
            max_decimal_digits (int): New maximum number of decimal places permitted in the input.
        """
        self._max_decimal_digits = max_decimal_digits
      
        # Base pattern for the integer part
        integer_pattern = "(0|[1-9][0-9]{0,6})"
    
        # Optional decimal part pattern, included only if max_decimal_digits > 0
        decimal_pattern = f"(\\.[0-9]{{1,{max_decimal_digits}}})" if max_decimal_digits > 0 else ""
    
        # Combine patterns. Make decimal part optional in regex if max_decimal_digits > 0
        pattern = f"^{integer_pattern}{decimal_pattern}?$" if max_decimal_digits > 0 else f"^{integer_pattern}$"

        self.validator = QRegularExpressionValidator(QRegularExpression(pattern))
    
    def get_validator(self) -> QRegularExpressionValidator:
        """
        Return the current validator.
        """
        return self.validator

    def validate(self, text: str) -> str:
        """
        Validate input text, ensuring it's a string or float and format it adequately.

        Args:
            text (str): The text to validate.

        Returns:
            validated_text (str): The validated text.
        """
        try:
            value = float(text)
            validated_text = self.validate_value(value)
        except (ValueError, TypeError):
            # If the conversion fails (ValueError) or if text is not a string (TypeError),
            # return an empty string
            validated_text = ''
        
        return validated_text
    
    def validate_value(self, value: float) -> str:
        """
        Validate input value, ensuring it's a positive number formatted to the specified precision.

        Args:
            value (float): The value to validate.

        Returns:
            validated_text (str): The validated value formatted to the specified precision, or an empty string if invalid.
        """
        if value > 0:
                # Round the value to the maximum allowed decimal digits
                rounded_value = round(value, self._max_decimal_digits)
                # Format the rounded value to a string with the specified number of decimal places
                validated_text = f'{rounded_value:.{self._max_decimal_digits}f}'
        else:
            # If the value is not positive, return an empty string
            validated_text = ''
        
        return validated_text
