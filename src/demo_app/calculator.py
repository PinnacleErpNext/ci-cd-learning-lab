"""Small business rules used to demonstrate automated testing."""


def calculate_discount(amount: float, customer_type: str) -> float:
    """Return the discount amount for a supported customer type."""
    if amount < 0:
        raise ValueError("amount cannot be negative")

    rates = {
        "regular": 0.00,
        "silver": 0.05,
        "gold": 0.10,
    }

    if customer_type not in rates:
        raise ValueError(f"Unsupported customer type: {customer_type}")

    return round(amount * rates[customer_type], 2)


def calculate_net_amount(amount: float, customer_type: str) -> float:
    """Return amount after discount."""
    return round(amount - calculate_discount(amount, customer_type), 2)
