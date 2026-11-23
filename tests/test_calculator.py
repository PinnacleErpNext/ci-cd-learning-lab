import pytest

from demo_app.calculator import calculate_discount, calculate_net_amount


def test_regular_customer_gets_no_discount():
    assert calculate_discount(1000, "regular") == 0


def test_silver_customer_gets_five_percent():
    assert calculate_discount(1000, "silver") == 50


def test_gold_customer_gets_ten_percent():
    assert calculate_discount(1000, "gold") == 100


def test_net_amount_after_gold_discount():
    assert calculate_net_amount(1000, "gold") == 900


def test_negative_amount_is_rejected():
    with pytest.raises(ValueError, match="negative"):
        calculate_discount(-1, "gold")


def test_unknown_customer_type_is_rejected():
    with pytest.raises(ValueError, match="Unsupported"):
        calculate_discount(1000, "platinum")
