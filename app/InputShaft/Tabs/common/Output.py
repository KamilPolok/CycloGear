from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QWidget

class Output(QLineEdit):
    """
    Custom QLineEdit that serves as output - it is readonly and 
    allows for setting the text only programtically.
    """

    def __init__(self, parent: QWidget=None, decimal_precision: int=2):
        super().__init__(parent)
        self.setReadOnly(True)
        self._max_decimal_digits = decimal_precision

    def setDecimalPrecision(self, decimal_precision):
        """
        Update the maximum decimal precision of the validator.

        Args:
            decimal_precision (int): New maximum number of decimal digits.
        """
        self._max_decimal_digits = decimal_precision
        self.setText(self.text())
    
    def setText(self, text: str):
        """
        Validate and set text.

        Args:
            text (str): The text to set.
        """
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        validated_text = text

        super().setText(validated_text)

    def setValue(self, value: float):
        """
        Validate and set value.

        Args:
            value (float): The value to set.
        """
        rounded_value = round(value, self._max_decimal_digits)
        validated_text = f'{rounded_value:.{self._max_decimal_digits}f}'
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        super().setText(validated_text)

    def value(self) -> Optional[float]:
        """
        Retutn value.

        Returns:
            (float | None): The value the input is holding
        """
        text = self.text()
        return None if text == "" else float(text)
