from decimal import Decimal
from unittest import TestCase

from app import create_app


class TestFormatUtils(TestCase):

    def setUp(self):
        self.app = create_app('default')
        self.currency_es_filter = self.app.jinja_env.filters['currency_es']

    def test_format_simple_decimal(self):
        result = self.currency_es_filter(Decimal("100.50"))
        assert result == "100,50 €"

    def test_format_integer(self):
        result = self.currency_es_filter(150)
        assert result == "150,00 €"

    def test_format_with_thousands_separator(self):
        result = self.currency_es_filter(Decimal("1234.56"))
        assert result == "1.234,56 €"

    def test_format_with_multiple_thousands(self):
        result = self.currency_es_filter(Decimal("1234567.89"))
        assert result == "1.234.567,89 €"

    def test_format_negative_number(self):
        result = self.currency_es_filter(Decimal("-150.50"))
        assert result == "-150,50 €"

    def test_format_negative_with_thousands(self):
        result = self.currency_es_filter(Decimal("-1234.56"))
        assert result == "-1.234,56 €"

    def test_format_zero(self):
        result = self.currency_es_filter(Decimal("0.00"))
        assert result == "0,00 €"

    def test_format_none_value(self):
        result = self.currency_es_filter(None)
        assert result == "0,00 €"

    def test_format_float(self):
        result = self.currency_es_filter(300.75)
        assert result == "300,75 €"

    def test_format_large_number(self):
        result = self.currency_es_filter(Decimal("999999999.99"))
        assert result == "999.999.999,99 €"


