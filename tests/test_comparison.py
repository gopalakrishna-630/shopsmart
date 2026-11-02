import unittest
from unittest.mock import MagicMock
from modules.comparison import ComparisonManager
from modules.recommendation import RecommendationManager

class TestComparisonAndRecommendation(unittest.TestCase):

    def setUp(self):
        self.mock_bm = MagicMock()
        self.mock_bm.get_budget_status.return_value = {
            "budget": 10000,
            "spent": 2000,
            "remaining": 8000,
            "usage_percent": 20,
            "status": "Normal"
        }
        self.mock_pm = MagicMock()
        self.products = [
            {"product_id": "P1", "name": "Prod 1", "price": 5000, "rating": 4.5, "category": "Electronics"},
            {"product_id": "P2", "name": "Prod 2", "price": 4000, "rating": 4.0, "category": "Electronics"},
            {"product_id": "P3", "name": "Prod 3", "price": 9000, "rating": 4.8, "category": "Electronics"}
        ]
        self.mock_pm.get_all_products.return_value = self.products
        
        self.cm = ComparisonManager(self.mock_bm, self.mock_pm)
        self.rm = RecommendationManager(self.cm)


    def test_compare_products(self):
        result = self.cm.compare_products(self.products)
        self.assertEqual(result["lowest_price"], 4000)
        self.assertEqual(result["highest_rating"], 4.8)
        
        ranked = result["ranked_results"]
        # P2 has lowest price (100 score), rating 4.0 (80 score), fits budget (100 score)
        # Score = 100*0.4 + 80*0.4 + 100*0.2 = 40 + 32 + 20 = 92.0
        
        # P1 price = 5000. max=9000, min=4000
        # price_score = 100 * (1 - (1000/5000)) = 100 * 0.8 = 80
        # rating = 4.5 -> 90 score
        # budget = fits -> 100 score
        # Score = 80*0.4 + 90*0.4 + 100*0.2 = 32 + 36 + 20 = 88.0
        
        self.assertEqual(ranked[0]["product"]["product_id"], "P2")

    def test_recommend_best_product(self):
        rec = self.rm.recommend_best_product(self.products)
        self.assertEqual(rec["recommended"]["product"]["product_id"], "P2")
        self.assertTrue(len(rec["alternatives"]) > 0)

if __name__ == "__main__":
    unittest.main()
