from typing import List, Dict, Any
from modules.comparison import ComparisonManager

class RecommendationManager:
    def __init__(self, comparison_manager: ComparisonManager):
        self.comparison_manager = comparison_manager

    def recommend_best_product(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Recommends the best product out of a given list based on purchase score."""
        if not products:
            return {}
            
        comparison_results = self.comparison_manager.compare_products(products)
        best_overall = comparison_results.get("best_overall")
        
        if not best_overall:
            return {}
            
        ranked_results = comparison_results.get("ranked_results", [])
        alternatives = [r for r in ranked_results if r["product"]["product_id"] != best_overall["product"]["product_id"]][:2]
        
        return {
            "recommended": best_overall,
            "alternatives": alternatives
        }
