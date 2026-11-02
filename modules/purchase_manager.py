from typing import List, Dict, Any, Optional
from datetime import datetime
from utils.storage import load_data, save_data
from utils.helpers import generate_id
from utils.validators import validate_purchase_data
from modules.product_manager import ProductManager

class PurchaseManager:
    def __init__(self, product_manager: ProductManager):
        self.purchases = load_data("purchases.json")
        self.product_manager = product_manager

    def save(self):
        return save_data("purchases.json", self.purchases)

    def add_purchase(self, product_id: str, quantity: int, date_str: str) -> tuple[bool, str]:
        product = self.product_manager.get_product_by_id(product_id)
        if not product:
            return False, "Product not found."
            
        unit_price = product["price"]
        
        valid, msg = validate_purchase_data(product_id, quantity, unit_price, date_str)
        if not valid:
            return False, msg

        if product.get("quantity", 0) < quantity:
            return False, f"Not enough quantity available. Available: {product.get('quantity', 0)}"

        total_price = quantity * unit_price
        purchase_id = generate_id("PUR")
        
        new_purchase = {
            "purchase_id": purchase_id,
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price,
            "purchase_date": date_str,
            "store": product["store"],
            "category": product["category"],
            "status": "completed"
        }
        
        self.purchases.append(new_purchase)
        
        # Deduct quantity from product
        self.product_manager.update_product(product_id, {"quantity": product["quantity"] - quantity})
        
        if self.save():
            return True, f"Purchase added successfully. Total: ₹{total_price:,.2f}"
        return False, "Failed to save purchase data."

    def get_all_purchases(self) -> List[Dict[str, Any]]:
        return self.purchases

    def get_purchase_by_id(self, purchase_id: str) -> Optional[Dict[str, Any]]:
        for p in self.purchases:
            if p["purchase_id"] == purchase_id:
                return p
        return None

    def cancel_purchase(self, purchase_id: str) -> tuple[bool, str]:
        purchase = self.get_purchase_by_id(purchase_id)
        if not purchase:
            return False, "Purchase not found."
            
        if purchase.get("status") == "cancelled":
            return False, "Purchase is already cancelled."
            
        purchase["status"] = "cancelled"
        
        # Restore quantity to product
        product = self.product_manager.get_product_by_id(purchase["product_id"])
        if product:
            self.product_manager.update_product(purchase["product_id"], {"quantity": product["quantity"] + purchase["quantity"]})
            
        if self.save():
            return True, "Purchase cancelled successfully."
        return False, "Failed to save purchase data."
