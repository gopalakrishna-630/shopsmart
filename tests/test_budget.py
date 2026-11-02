import unittest
from unittest.mock import patch, MagicMock
from modules.budget_manager import BudgetManager

class TestBudgetManager(unittest.TestCase):

    @patch("modules.budget_manager.load_data", side_effect=lambda x: {"budget": 10000.0})
    @patch("modules.budget_manager.save_data", return_value=True)
    def setUp(self, mock_save, mock_load):
        self.mock_pur_m = MagicMock()
        self.mock_pur_m.get_all_purchases.return_value = [
            {"total_price": 2000, "status": "completed"},
            {"total_price": 1500, "status": "completed"},
            {"total_price": 500, "status": "cancelled"}
        ]
        
        self.bm = BudgetManager(self.mock_pur_m)

    @patch("modules.budget_manager.save_data", return_value=True)
    def test_set_budget(self, mock_save):
        success, msg = self.bm.set_budget(15000)
        self.assertTrue(success)
        self.assertEqual(self.bm.get_budget(), 15000)

    def test_get_total_spending(self):
        self.assertEqual(self.bm.get_total_spending(), 3500)

    def test_budget_status(self):
        status = self.bm.get_budget_status()
        self.assertEqual(status["budget"], 10000)
        self.assertEqual(status["spent"], 3500)
        self.assertEqual(status["remaining"], 6500)
        self.assertEqual(status["usage_percent"], 35.0)
        self.assertEqual(status["status"], "Normal")

if __name__ == "__main__":
    unittest.main()
