import uuid

def generate_id(prefix: str) -> str:
    """Generate a unique ID with a given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

def format_currency(amount: float) -> str:
    """Format float as INR currency."""
    return f"₹{amount:,.2f}"
