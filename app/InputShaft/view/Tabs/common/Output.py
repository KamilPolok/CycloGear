from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

class Output(QLineEdit):
    """Custom QLineEdit that serves as output - it is readonly and 
       allows for setting the text only programtically.
    """

    def __init__(self, parent=None, text = '', decimal_precision = 2):
        super().__init__(parent)
        self._max_decimal_digits = decimal_precision

        if text:
            self.setText(text)

    def setDecimalPrecision(self, decimal_precision):
        """Updates the maximum decimal precision of the validator.

        Args:
            decimal_precision (int): New maximum number of decimal digits.
        """
        self._max_decimal_digits = decimal_precision
        self.setText(self.text())
    
    def setText(self, text):
        """Validates and sets the text.
        Args:
            text (str): The text to set.
        """
        try:
            value = float(text)
            rounded_value = round(value, self._max_decimal_digits)
            validated_text = f'{rounded_value:.{self._max_decimal_digits}f}'
            self.setAlignment(Qt.AlignmentFlag.AlignRight)
        except ValueError:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            validated_text = text
        except TypeError:
            validated_text = ''

        super().setText(validated_text)
