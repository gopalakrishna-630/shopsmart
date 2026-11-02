import unittest
from unittest.mock import patch, mock_open
from modules.product_manager import ProductManager

class TestProductManager(unittest.TestCase):

    @patch("modules.product_manager.load_data", side_effect=lambda x: [])
    @patch("modules.product_manager.save_data", return_value=True)
    def setUp(self, mock_save, mock_load):
        self.pm = ProductManager()

    @patch("modules.product_manager.save_data", return_value=True)
    def test_add_product(self, mock_save):
        success, msg = self.pm.add_product("Sony", "Electronics", 2499, 10, "Amazon", 4.5)
        self.assertTrue(success)
        self.assertEqual(len(self.pm.get_all_products()), 1)

    @patch("modules.product_manager.save_data", return_value=True)
    def test_add_invalid_product(self, mock_save):
        success, msg = self.pm.add_product("", "Electronics", -10, 10, "Amazon", 4.5)
        self.assertFalse(success)
        self.assertEqual(len(self.pm.get_all_products()), 0)

    @patch("modules.product_manager.save_data", return_value=True)
    def test_search_and_filter(self, mock_save):
        self.pm.add_product("Sony Headphones", "Electronics", 2499, 10, "Amazon", 4.5)
        self.pm.add_product("JBL Headphones", "Electronics", 1599, 5, "Flipkart", 4.2)
        self.pm.add_product("T-shirt", "Clothing", 500, 20, "Myntra", 4.0)

        results = self.pm.search_products("headphone")
        self.assertEqual(len(results), 2)

        filtered = self.pm.filter_products(category="Electronics", min_price=2000)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "Sony Headphones")

if __name__ == "__main__":
    unittest.main()
