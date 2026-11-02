from datetime import datetime

def validate_product_data(name: str, price: float, quantity: int, rating: float) -> tuple[bool, str]:
    if not name or not str(name).strip():
        return False, "Product name cannot be empty."
    if not isinstance(price, (int, float)) or price < 0:
        return False, "Price must be numeric and >= 0."
    if not isinstance(quantity, int) or quantity < 0:
        return False, "Quantity must be a non-negative integer."
    if not isinstance(rating, (int, float)) or not (0 <= rating <= 5):
        return False, "Rating must be between 0 and 5."
    return True, ""

def validate_purchase_data(product_id: str, quantity: int, unit_price: float, date_str: str) -> tuple[bool, str]:
    if not product_id or not str(product_id).strip():
        return False, "Product ID cannot be empty."
    if not isinstance(quantity, int) or quantity <= 0:
        return False, "Quantity must be a positive integer."
    if not isinstance(unit_price, (int, float)) or unit_price < 0:
        return False, "Unit price must be numeric and >= 0."
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False, "Date must use a valid format (YYYY-MM-DD)."
    return True, ""
