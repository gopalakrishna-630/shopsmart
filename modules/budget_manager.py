from typing import Dict, Any
from utils.storage import load_data, save_data
from modules.purchase_manager import PurchaseManager

class BudgetManager:
    def __init__(self, purchase_manager: PurchaseManager):
        # budget.json structure: {"budget": 10000.0}
        self.budget_data = load_data("budget.json")
        self.purchase_manager = purchase_manager

    def save(self):
        return save_data("budget.json", self.budget_data)

    def set_budget(self, amount: float) -> tuple[bool, str]:
        if not isinstance(amount, (int, float)) or amount < 0:
            return False, "Budget must be a non-negative number."
            
        self.budget_data["budget"] = float(amount)
        if self.save():
            return True, f"Budget set successfully to ₹{amount:,.2f}"
        return False, "Failed to save budget data."

    def get_budget(self) -> float:
        return self.budget_data.get("budget", 0.0)

    def get_total_spending(self) -> float:
        purchases = self.purchase_manager.get_all_purchases()
        return sum(p["total_price"] for p in purchases if p.get("status") != "cancelled")

    def get_budget_status(self) -> Dict[str, Any]:
        budget = self.get_budget()
        spent = self.get_total_spending()
        remaining = budget - spent
        
        usage_percent = (spent / budget * 100) if budget > 0 else 0
        
        if usage_percent < 75:
            status = "Normal"
        elif usage_percent <= 90:
            status = "Warning"
        elif usage_percent <= 100:
            status = "High spending warning"
        else:
            status = "Budget exceeded"
            
        return {
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "usage_percent": usage_percent,
            "status": status
        }
