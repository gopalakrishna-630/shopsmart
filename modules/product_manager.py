from typing import List, Dict, Any, Optional
from utils.storage import load_data, save_data
from utils.helpers import generate_id
from utils.validators import validate_product_data

class ProductManager:
    def __init__(self):
        self.products = load_data("products.json")

    def save(self):
        return save_data("products.json", self.products)

    def add_product(self, name: str, category: str, price: float, quantity: int, store: str, rating: float, description: str = "") -> tuple[bool, str]:
        valid, msg = validate_product_data(name, price, quantity, rating)
        if not valid:
            return False, msg
            
        product_id = generate_id("P")
        new_product = {
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "store": store,
            "rating": rating,
            "description": description
        }
        self.products.append(new_product)
        if self.save():
            return True, f"Product added successfully. ID: {product_id}"
        return False, "Failed to save product data."

    def get_all_products(self) -> List[Dict[str, Any]]:
        return self.products

    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        for p in self.products:
            if p["product_id"] == product_id:
                return p
        return None

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> tuple[bool, str]:
        product = self.get_product_by_id(product_id)
        if not product:
            return False, "Product not found."
            
        # validate updates if any critical fields are being updated
        # for simplicity, we assume we validate before calling update_product or we do it here
        name = updates.get("name", product["name"])
        price = updates.get("price", product["price"])
        quantity = updates.get("quantity", product["quantity"])
        rating = updates.get("rating", product["rating"])
        
        valid, msg = validate_product_data(name, price, quantity, rating)
        if not valid:
            return False, msg

        product.update(updates)
        if self.save():
            return True, "Product updated successfully."
        return False, "Failed to save product data."

    def delete_product(self, product_id: str) -> tuple[bool, str]:
        product = self.get_product_by_id(product_id)
        if not product:
            return False, "Product not found."
            
        self.products = [p for p in self.products if p["product_id"] != product_id]
        if self.save():
            return True, "Product deleted successfully."
        return False, "Failed to save product data."

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower().strip()
        if not q:
            return self.products
            
        words = q.split()
        results = []
        
        for p in self.products:
            score = 0
            name = p.get("name", "").lower()
            pid = p.get("product_id", "").lower()
            cat = p.get("category", "").lower()
            store = p.get("store", "").lower()
            desc = p.get("description", "").lower()
            
            # Exact full-query matches
            if q == name or q == pid:
                score += 100
            elif q in name:
                score += 50
            elif q in desc:
                score += 20
                
            # Individual word matching
            matched_words = 0
            for w in words:
                if w in name:
                    score += 10
                    matched_words += 1
                elif w in cat or w in store:
                    score += 5
                    matched_words += 1
                elif w in desc or w in pid:
                    score += 2
                    matched_words += 1
                    
            if score > 0:
                # Bonus if all words are found somewhere in the product
                if matched_words == len(words) and len(words) > 1:
                    score += 30
                results.append((score, p))
                
        # Sort by relevance score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]

    def filter_products(self, category: str = None, store: str = None, 
                        min_price: float = None, max_price: float = None, 
                        min_rating: float = None, max_rating: float = None) -> List[Dict[str, Any]]:
        results = []
        for p in self.products:
            if category and category.lower() != p["category"].lower():
                continue
            if store and store.lower() != p["store"].lower():
                continue
            if min_price is not None and p["price"] < min_price:
                continue
            if max_price is not None and p["price"] > max_price:
                continue
            if min_rating is not None and p["rating"] < min_rating:
                continue
            if max_rating is not None and p["rating"] > max_rating:
                continue
            results.append(p)
        return results
