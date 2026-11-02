from typing import Dict, Any, List
from modules.product_manager import ProductManager
from modules.purchase_manager import PurchaseManager
from modules.budget_manager import BudgetManager

class AnalyticsManager:
    def __init__(self, product_manager: ProductManager, purchase_manager: PurchaseManager, budget_manager: BudgetManager):
        self.product_manager = product_manager
        self.purchase_manager = purchase_manager
        self.budget_manager = budget_manager

    def get_overall_analytics(self) -> Dict[str, Any]:
        products = self.product_manager.get_all_products()
        purchases = [p for p in self.purchase_manager.get_all_purchases() if p.get("status") != "cancelled"]
        
        total_spent = sum(p["total_price"] for p in purchases)
        total_items = sum(p["quantity"] for p in purchases)
        
        budget_status = self.budget_manager.get_budget_status()
        
        highest_purchase = max(purchases, key=lambda x: x["total_price"], default=None)
        lowest_purchase = min(purchases, key=lambda x: x["total_price"], default=None)
        
        return {
            "total_products": len(products),
            "total_purchases": len(purchases),
            "total_items_purchased": total_items,
            "total_spent": total_spent,
            "average_purchase": (total_spent / len(purchases)) if purchases else 0,
            "highest_purchase": highest_purchase["total_price"] if highest_purchase else 0,
            "lowest_purchase": lowest_purchase["total_price"] if lowest_purchase else 0,
            "budget": budget_status["budget"],
            "remaining_budget": budget_status["remaining"],
            "budget_usage": budget_status["usage_percent"]
        }

    def get_category_spending(self) -> Dict[str, Any]:
        purchases = [p for p in self.purchase_manager.get_all_purchases() if p.get("status") != "cancelled"]
        category_totals = {}
        for p in purchases:
            cat = p.get("category", "Other")
            category_totals[cat] = category_totals.get(cat, 0) + p["total_price"]
            
        total_spent = sum(category_totals.values())
        
        percentages = {cat: (amount / total_spent * 100) if total_spent > 0 else 0 
                       for cat, amount in category_totals.items()}
                       
        highest_category = max(category_totals.items(), key=lambda x: x[1], default=("None", 0))
        lowest_category = min(category_totals.items(), key=lambda x: x[1], default=("None", 0))
        
        return {
            "totals": category_totals,
            "percentages": percentages,
            "highest_category": highest_category,
            "lowest_category": lowest_category
        }

    def get_store_spending(self) -> Dict[str, Any]:
        purchases = [p for p in self.purchase_manager.get_all_purchases() if p.get("status") != "cancelled"]
        store_totals = {}
        store_counts = {}
        
        for p in purchases:
            store = p.get("store", "Unknown")
            store_totals[store] = store_totals.get(store, 0) + p["total_price"]
            store_counts[store] = store_counts.get(store, 0) + 1
            
        store_averages = {store: store_totals[store] / store_counts[store] for store in store_totals}
        
        highest_store = max(store_totals.items(), key=lambda x: x[1], default=("None", 0))
        
        return {
            "totals": store_totals,
            "counts": store_counts,
            "averages": store_averages,
            "highest_store": highest_store
        }

    def get_purchase_history(self, sort_by: str = "date", reverse: bool = True) -> List[Dict[str, Any]]:
        purchases = self.purchase_manager.get_all_purchases()
        
        if sort_by == "price":
            return sorted(purchases, key=lambda x: x["total_price"], reverse=reverse)
        elif sort_by == "category":
            return sorted(purchases, key=lambda x: x.get("category", ""), reverse=reverse)
        elif sort_by == "store":
            return sorted(purchases, key=lambda x: x.get("store", ""), reverse=reverse)
        else: # date
            return sorted(purchases, key=lambda x: x["purchase_date"], reverse=reverse)
