from typing import List, Dict, Any
from modules.budget_manager import BudgetManager
from modules.product_manager import ProductManager

class ComparisonManager:
    def __init__(self, budget_manager: BudgetManager, product_manager: ProductManager):
        self.budget_manager = budget_manager
        self.product_manager = product_manager

    def compare_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not products:
            return {}
            
        lowest_price = min(p["price"] for p in products)
        highest_rating = max(p["rating"] for p in products)
        
        results = []
        for p in products:
            results.append({
                "product": p,
                "score_details": self.calculate_purchase_score(p, products)
            })
            
        # Sort products based on final score descending
        results.sort(key=lambda x: x["score_details"]["score"], reverse=True)
        
        return {
            "lowest_price": lowest_price,
            "highest_rating": highest_rating,
            "best_overall": results[0] if results else None,
            "ranked_results": results
        }

    def calculate_purchase_score(self, product: Dict[str, Any], comparison_set: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate an advanced purchase score based on:
        1. Rating (30%)
        2. Price Competitiveness (30%) - Compared to average of its category
        3. Value for Money (20%) - Rating per currency unit compared to category
        4. Budget Compliance (20%) - Checks if it fits the remaining budget
        """
        category = product.get("category", "")
        all_products = self.product_manager.get_all_products()
        category_products = [p for p in all_products if p.get("category", "").lower() == category.lower()]
        
        # Fallback if no products in category
        if not category_products:
            category_products = [product]
            
        avg_category_price = sum(p["price"] for p in category_products) / len(category_products)
        avg_category_rating = sum(p["rating"] for p in category_products) / len(category_products)
        
        # 1. Price Competitiveness Score (0-100)
        # Compares product price against the market average in its category
        if avg_category_price == 0:
            price_score = 100.0
        else:
            ratio = product["price"] / avg_category_price
            if ratio <= 0.5:
                price_score = 100.0
            elif ratio >= 2.0:
                price_score = 0.0
            else:
                # Linear scale where ratio=1.0 is ~66 score
                price_score = 100.0 - ((ratio - 0.5) / 1.5) * 100.0
                
        # 2. Rating Score (0-100)
        rating_score = (product["rating"] / 5.0) * 100.0
        
        # 3. Value for Money Score (0-100)
        if avg_category_price > 0 and avg_category_rating > 0:
            avg_value = avg_category_rating / avg_category_price
            prod_value = product["rating"] / product["price"] if product["price"] > 0 else 0
            
            value_ratio = prod_value / avg_value if avg_value > 0 else 1.0
            
            if value_ratio >= 1.5:
                value_score = 100.0
            elif value_ratio <= 0.5:
                value_score = 0.0
            else:
                value_score = ((value_ratio - 0.5) / 1.0) * 100.0
        else:
            value_score = 70.0  # Safe default if maths fail (e.g., zero price)
            
        # 4. Budget Score (0-100)
        budget_status = self.budget_manager.get_budget_status()
        remaining_budget = budget_status["remaining"]
        
        if budget_status["budget"] == 0:
            budget_score = 100.0
        elif product["price"] <= remaining_budget:
            budget_score = 100.0
        else:
            overage = product["price"] - remaining_budget
            penalty = (overage / budget_status["budget"]) * 100
            budget_score = max(0.0, 100.0 - penalty)
            
        # Calculate Weighted Final Score
        final_score = (price_score * 0.30) + (rating_score * 0.30) + (value_score * 0.20) + (budget_score * 0.20)
        
        # Generate Smart Reasons
        reasons = []
        if rating_score >= 80:
            reasons.append("✓ Strong customer rating")
        if price_score >= 75:
            reasons.append("✓ Highly competitive price in its category")
        if value_score >= 80:
            reasons.append("✓ Excellent value for money")
        if budget_score == 100:
            reasons.append("✓ Fits comfortably within current budget")
        elif budget_score < 50:
            reasons.append("⚠ Significantly exceeds available budget")
            
        return {
            "score": round(final_score, 1),
            "price_score": round(price_score, 1),
            "rating_score": round(rating_score, 1),
            "value_score": round(value_score, 1),
            "budget_score": round(budget_score, 1),
            "reasons": reasons
        }
