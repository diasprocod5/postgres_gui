from PySide6.QtGui import  QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class Validators:
    patterns = {
        'full_name': r"^([А-ЯЁ][а-яё]{0,20}\s){2}[А-ЯЁ][а-яё]{0,20}$",
        'phone': r"^9[0-9]{9}$",
        'balance': r"^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$|^0\.[0-9]{1,2}$",
        'tariff_name': r'^.{5,25}$',
        'tariff_price': r"^[1-9][0-9]{1,4}(\.[0-9]{1,2})?$",
        'amount': r"^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$",
    }

    @classmethod
    def get_validator(cls, field_name:str):
        pattern = cls.patterns.get(field_name)
        if not pattern:
            raise  ValueError(f"No pattern defined for '{field_name}'")
        return QRegularExpressionValidator(QRegularExpression(pattern))