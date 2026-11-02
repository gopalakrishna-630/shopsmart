import unittest
from unittest.mock import patch, MagicMock
from modules.purchase_manager import PurchaseManager

class TestPurchaseManager(unittest.TestCase):

    @patch("modules.purchase_manager.load_data", side_effect=lambda x: [])
    @patch("modules.purchase_manager.save_data", return_value=True)
    def setUp(self, mock_save, mock_load):
        self.mock_pm = MagicMock()
        self.mock_pm.get_product_by_id.return_value = {
            "product_id": "P001",
            "name": "Sony WH-CH520",
            "price": 2499,
            "quantity": 10,
            "store": "Amazon",
            "category": "Electronics"
        }
        self.mock_pm.update_product.return_value = (True, "")
        
        self.pur_m = PurchaseManager(self.mock_pm)

    @patch("modules.purchase_manager.save_data", return_value=True)
    def test_add_purchase(self, mock_save):
        success, msg = self.pur_m.add_purchase("P001", 2, "2026-08-24")
        self.assertTrue(success)
        purchases = self.pur_m.get_all_purchases()
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases[0]["total_price"], 4998)
        self.mock_pm.update_product.assert_called_with("P001", {"quantity": 8})

    @patch("modules.purchase_manager.save_data", return_value=True)
    def test_add_purchase_insufficient_quantity(self, mock_save):
        success, msg = self.pur_m.add_purchase("P001", 15, "2026-08-24")
        self.assertFalse(success)
        self.assertIn("Not enough quantity", msg)
        self.assertEqual(len(self.pur_m.get_all_purchases()), 0)

if __name__ == "__main__":
    unittest.main()
