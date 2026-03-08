import pytest
from datetime import datetime
from pydantic import ValidationError
from app.data_contract import Orders


def test_orders_with_valid_data():
    """
    Function that tests the creation of an instance of the Orders class with valid data.
    Valid data includes a correct e-mail address, date in the correct format, positive order value, a product name, positive quantity and an existing product category.
    The test will confirm if the values stored in the instance match the data provided.
    """
    valid_data = {
        "customer_email": "customer@example.com",
        "order_date": datetime.now(),
        "order_value": 100.50,
        "product": "ABC",
        "quantity": 4,
        "category": "category1",
    }

    order = Orders(**valid_data)

    assert order.email == valid_data["customer_email"]
    assert order.order_date == valid_data["order_date"]
    assert order.order_value == valid_data["order_value"]
    assert order.product == valid_data["product"]
    assert order.quantity == valid_data["quantity"]
    assert order.category == valid_data["category"]


def test_orders_with_invalid_data():
    """
    Function that tests the creation of an instance of the Orders class with invalid data.
    Invalid data includes a incorrect e-mail address, date in the incorrect format, negative order value, no product name, negative quantity and an invalid product category.
    The Orders class is expected to raise a ValidationError exception when invalid data is provided.
    """
    invalid_data = {
        "customer_email": "john doe",
        "order_date": "20251203",
        "order_value": -100,
        "product": "",
        "quantity": -2,
        "category": "category78",
    }

    with pytest.raises(ValidationError):
        Orders(**invalid_data)


def test_category_validation():
    """
    Function that tests the category validation when creating an instance of the Orders class.
    It uses valid data for all fields except for the category, which is set to a non-existent category.
    The Orders class is expected to raise a ValidationError exception due to the invalid category.
    """
    order_data = {
        "customer_email": "customer@example.com",
        "order_date": datetime.now(),
        "order_value": 100.50,
        "product": "ABCD",
        "quantity": 4,
        "category": "random category",
    }

    with pytest.raises(ValidationError):
        Orders(**order_data)
