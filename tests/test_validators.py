import pytest
from PySide6.QtGui import QValidator
from validators import Validators

test_cases = [
    ('full_name', 'Иванов Иван Иванович', QValidator.State.Acceptable),
    ('full_name', 'Ильф И Петров ', QValidator.State.Invalid),
    ('phone', '9123456789', QValidator.State.Acceptable),
    ('phone', '8123456789', QValidator.State.Invalid),
    ('balance', '100.50', QValidator.State.Acceptable),
    ('balance', '0.123', QValidator.State.Invalid),
    ('tariff_name', 'Базовый тариф', QValidator.State.Acceptable),
    ('tariff_name', 'New', QValidator.State.Intermediate),
    ('tariff_price', '1999.99', QValidator.State.Acceptable),
    ('amount', '10.01', QValidator.State.Acceptable),
    ('amount', '0.123', QValidator.State.Invalid),
]

@pytest.mark.parametrize("field, value, expected", test_cases)
def test_validators(field, value, expected):
    validator = Validators.get_validator(field)
    state, _, _ = validator.validate(value, 0)
    assert state == expected