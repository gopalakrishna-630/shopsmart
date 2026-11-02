import sys
import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from modules.product_manager import ProductManager
from modules.purchase_manager import PurchaseManager
from modules.budget_manager import BudgetManager
from modules.comparison import ComparisonManager
from modules.recommendation import RecommendationManager
from modules.analytics import AnalyticsManager
from modules.reports import ReportManager
from utils.storage import create_backup, list_backups, restore_backup
from utils.helpers import format_currency

console = Console()

def interactive_menu(title: str, choices_with_values: list[tuple[str, str]]) -> str:
    """Safe wrapper around questionary to handle environments without full interactive support."""
    choices = [Choice(title=k, value=v) for k, v in choices_with_values]
    try:
        answer = questionary.select(title, choices=choices).ask()
        if answer is None:
            # find the exit or back value
            for k, v in choices_with_values:
                if "Exit" in k or "Back" in k:
                    return v
            return choices_with_values[-1][1]
        return answer
    except Exception:
        # Fallback to standard input if questionary fails (e.g. not a TTY)
        print(f"\n{title}")
        for k, v in choices_with_values:
            print(k)
        try:
            return input("Select an option (enter number/value): ").strip()
        except (EOFError, KeyboardInterrupt):
            for k, v in choices_with_values:
                if "Exit" in k or "Back" in k:
                    return v
            return choices_with_values[-1][1]

def interactive_input(prompt: str) -> str:
    """Safe text input wrapper using questionary."""
    try:
        # questionary.text handles arrow keys natively
        ans = questionary.text(prompt).ask()
        return ans.strip() if ans is not None else ""
    except Exception:
        try:
            return input(f"{prompt} ").strip()
        except:
            return ""

def interactive_multiselect(title: str, choices_with_values: list[tuple[str, str]]) -> list[str]:
    """Safe wrapper around questionary checkbox for multi-selection."""
    choices = [Choice(title=k, value=v) for k, v in choices_with_values]
    try:
        answer = questionary.checkbox(title, choices=choices).ask()
        if answer is None:
            return []
        return answer
    except Exception:
        # Fallback to manual entry
        print(f"\n{title}")
        for k, v in choices_with_values:
            print(f"- {k} (ID: {v})")
        try:
            val = input("Enter IDs separated by commas: ").strip()
            return [v.strip() for v in val.split(",") if v.strip()]
        except (EOFError, KeyboardInterrupt):
            return []

class ShopSmartApp:
    def __init__(self):
        self.product_manager = ProductManager()
        self.purchase_manager = PurchaseManager(self.product_manager)
        self.budget_manager = BudgetManager(self.purchase_manager)
        self.comparison_manager = ComparisonManager(self.budget_manager, self.product_manager)
        self.recommendation_manager = RecommendationManager(self.comparison_manager)
        self.analytics_manager = AnalyticsManager(self.product_manager, self.purchase_manager, self.budget_manager)
        self.report_manager = ReportManager(self.analytics_manager)

    def display_menu(self):
        console.print(Panel("[bold cyan]SHOPSMART – SMART PURCHASE OPTIMIZER[/bold cyan]", expand=False))
        options = [
            ("1. Product Management", "1"),
            ("2. Purchase Management", "2"),
            ("3. Search & Filter", "3"),
            ("4. Compare Products", "4"),
            ("5. Budget Management", "5"),
            ("6. Smart Recommendation", "6"),
            ("7. Analytics", "7"),
            ("8. Reports", "8"),
            ("9. Backup & Restore", "9"),
            ("10. Exit", "10")
        ]
        return interactive_menu("Main Menu (Use ↑/↓ and Enter to select):", options)

    def run(self):
        while True:
            console.clear()
            choice = self.display_menu()
            console.clear()
            try:
                if choice == "1":
                    self.product_menu()
                elif choice == "2":
                    self.purchase_menu()
                elif choice == "3":
                    self.search_filter_menu()
                elif choice == "4":
                    self.compare_menu()
                elif choice == "5":
                    self.budget_menu()
                elif choice == "6":
                    self.recommendation_menu()
                elif choice == "7":
                    self.analytics_menu()
                elif choice == "8":
                    self.reports_menu()
                elif choice == "9":
                    self.backup_restore_menu()
                elif choice == "10":
                    console.print("[green]Exiting ShopSmart. Goodbye![/green]")
                    sys.exit(0)
                else:
                    console.print("[red]Invalid choice. Please select a valid option.[/red]")
            except Exception as e:
                console.print(f"[red]An error occurred: {str(e)}[/red]")
                
            if choice != "10":
                print("\n")
                console.input("[dim]Press Enter to return to the main menu...[/dim]")

    def product_menu(self):
        options = [
            ("1. Add Product", "1"),
            ("2. View All Products", "2"),
            ("3. Delete Product", "3"),
            ("4. Back", "4")
        ]
        c = interactive_menu("--- PRODUCT MANAGEMENT ---", options)
        console.clear()
        
        if c == "1":
            name = interactive_input("Name:")
            while not name.strip() or name.isdigit():
                console.print("[red]Name must be a valid string, not just numbers.[/red]")
                name = interactive_input("Name:")

            cat_options = [
                ("1. Electronics", "Electronics"),
                ("2. Clothing", "Clothing"),
                ("3. Groceries", "Groceries"),
                ("4. Books", "Books"),
                ("5. Home Appliances", "Home Appliances"),
                ("6. Stationery", "Stationery"),
                ("7. Other", "Other")
            ]
            category = interactive_menu("Select Category:", cat_options)
            
            while True:
                try:
                    price = float(interactive_input("Price:"))
                    if price < 0:
                        console.print("[red]Price must be >= 0.[/red]")
                        continue
                    break
                except ValueError:
                    console.print("[red]Please enter a valid numeric price.[/red]")
            
            while True:
                try:
                    quantity = int(interactive_input("Quantity:"))
                    if quantity < 0:
                        console.print("[red]Quantity must be >= 0.[/red]")
                        continue
                    break
                except ValueError:
                    console.print("[red]Please enter a valid integer quantity.[/red]")
            
            while True:
                try:
                    rating = float(interactive_input("Rating (0-5):"))
                    if 0 <= rating <= 5:
                        break
                    console.print("[red]Rating must be between 0 and 5.[/red]")
                except ValueError:
                    console.print("[red]Please enter a valid number for rating.[/red]")
            
            store = interactive_input("Store:")
            while not store.strip() or store.isdigit():
                console.print("[red]Store must be a valid string, not just numbers.[/red]")
                store = interactive_input("Store:")
                
            desc = interactive_input("Description:")
            while not desc.strip() or desc.isdigit():
                console.print("[red]Description must be a valid string, not just numbers.[/red]")
                desc = interactive_input("Description:")
            
            success, msg = self.product_manager.add_product(name, category, price, quantity, store, rating, desc)
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")
            
        elif c == "2":
            products = self.product_manager.get_all_products()
            if not products:
                console.print("[yellow]No products available.[/yellow]")
                return
            table = Table(title="All Products")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Category")
            table.add_column("Price", justify="right")
            table.add_column("Qty", justify="right")
            table.add_column("Rating", justify="right")
            
            for p in products:
                table.add_row(p["product_id"], p["name"], p["category"], format_currency(p["price"]), str(p["quantity"]), str(p["rating"]))
            console.print(table)
            
        elif c == "3":
            pid = interactive_input("Enter Product ID to delete:")
            success, msg = self.product_manager.delete_product(pid)
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")

    def purchase_menu(self):
        options = [
            ("1. Add Purchase", "1"),
            ("2. View Purchases", "2"),
            ("3. Cancel Purchase", "3"),
            ("4. Back", "4")
        ]
        c = interactive_menu("--- PURCHASE MANAGEMENT ---", options)
        console.clear()
        
        if c == "1":
            pid = interactive_input("Product ID:")
            try:
                qty = int(interactive_input("Quantity:"))
            except ValueError:
                console.print("[red]Invalid quantity.[/red]")
                return
            date_str = interactive_input("Date (YYYY-MM-DD):")
            
            success, msg = self.purchase_manager.add_purchase(pid, qty, date_str)
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")
            
        elif c == "2":
            purchases = self.purchase_manager.get_all_purchases()
            if not purchases:
                console.print("[yellow]No purchases available.[/yellow]")
                return
            table = Table(title="Purchase History")
            table.add_column("ID", style="cyan")
            table.add_column("Product", style="magenta")
            table.add_column("Qty", justify="right")
            table.add_column("Total", justify="right")
            table.add_column("Date")
            table.add_column("Status")
            
            for p in purchases:
                table.add_row(p["purchase_id"], p["product_name"], str(p["quantity"]), format_currency(p["total_price"]), p["purchase_date"], p.get("status", "completed"))
            console.print(table)
            
        elif c == "3":
            pid = interactive_input("Enter Purchase ID to cancel:")
            success, msg = self.purchase_manager.cancel_purchase(pid)
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")

    def search_filter_menu(self):
        options = [
            ("1. Search by keyword", "1"),
            ("2. Filter by criteria", "2"),
            ("3. Back", "3")
        ]
        c = interactive_menu("--- SEARCH & FILTER ---", options)
        console.clear()
        
        if c == "1":
            q = interactive_input("Search query:")
            results = self.product_manager.search_products(q)
            self._display_product_table(results)
        elif c == "2":
            cat_options = [
                ("1. Any Category", "Any"),
                ("2. Electronics", "Electronics"),
                ("3. Clothing", "Clothing"),
                ("4. Groceries", "Groceries"),
                ("5. Books", "Books"),
                ("6. Home Appliances", "Home Appliances"),
                ("7. Stationery", "Stationery"),
                ("8. Other", "Other")
            ]
            cat_choice = interactive_menu("Category:", cat_options)
            cat = None if cat_choice == "Any" else cat_choice
            
            min_p = interactive_input("Min price (leave empty to skip):")
            max_p = interactive_input("Max price (leave empty to skip):")
            
            try:
                min_p = float(min_p) if min_p else None
                max_p = float(max_p) if max_p else None
            except ValueError:
                console.print("[red]Invalid numeric input.[/red]")
                return
                
            results = self.product_manager.filter_products(category=cat, min_price=min_p, max_price=max_p)
            self._display_product_table(results)

    def _display_product_table(self, products):
        if not products:
            console.print("[yellow]No products found.[/yellow]")
            return
        table = Table(title="Search Results")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Category")
        table.add_column("Store")
        table.add_column("Price", justify="right")
        table.add_column("Rating", justify="right")
        for p in products:
            table.add_row(p["product_id"], p["name"], p["category"], p.get("store", ""), format_currency(p["price"]), str(p["rating"]))
        console.print(table)

    def compare_menu(self):
        console.print("\n[bold]Compare Products[/bold]")
        
        all_products = self.product_manager.get_all_products()
        if len(all_products) < 2:
            console.print("[red]Not enough products to compare. Need at least 2 in the system.[/red]")
            return
            
        options = [(f"{p['name']} ({format_currency(p['price'])})", p["product_id"]) for p in all_products]
        
        selected_ids = interactive_multiselect("Select products to compare (Use Space to select, Enter to confirm):", options)
        console.clear()
        
        if len(selected_ids) < 2:
            console.print("[red]Need at least 2 valid products to compare.[/red]")
            return
            
        products = [self.product_manager.get_product_by_id(pid) for pid in selected_ids]
            
        results = self.comparison_manager.compare_products(products)
        
        table = Table(title="PRODUCT COMPARISON")
        table.add_column("Product Name")
        table.add_column("Price")
        table.add_column("Rating")
        table.add_column("Value")
        table.add_column("Score", style="green")
        
        for r in results["ranked_results"]:
            p = r["product"]
            score = r["score_details"]["score"]
            value = r["score_details"]["value_score"]
            table.add_row(p["name"], format_currency(p["price"]), str(p["rating"]), f"{value}/100", f"{score}/100")
            
        console.print(table)
        console.print(f"[bold cyan]Best Overall:[/bold cyan] {results['best_overall']['product']['name']}")

    def budget_menu(self):
        options = [
            ("1. Set Budget", "1"),
            ("2. View Budget Status", "2"),
            ("3. Back", "3")
        ]
        c = interactive_menu("--- BUDGET MANAGEMENT ---", options)
        console.clear()
        
        if c == "1":
            try:
                amt_str = interactive_input("Enter new budget amount:")
                amt = float(amt_str)
                success, msg = self.budget_manager.set_budget(amt)
                color = "green" if success else "red"
                console.print(f"[{color}]{msg}[/{color}]")
            except ValueError:
                console.print("[red]Invalid numeric input.[/red]")
        elif c == "2":
            status = self.budget_manager.get_budget_status()
            
            color = "green"
            if status["usage_percent"] > 90:
                color = "red"
            elif status["usage_percent"] > 75:
                color = "yellow"
                
            panel = Panel(
                f"Budget: {format_currency(status['budget'])}\n"
                f"Spent: {format_currency(status['spent'])}\n"
                f"Remaining: {format_currency(status['remaining'])}\n"
                f"Usage: {status['usage_percent']:.1f}%\n"
                f"Status: [{color}]{status['status']}[/{color}]",
                title="MONTHLY BUDGET"
            )
            console.print(panel)

    def recommendation_menu(self):
        console.print("\n[bold]Smart Recommendation[/bold]")
        products = self.product_manager.get_all_products()
        if len(products) < 2:
            console.print("[red]Not enough products for a recommendation.[/red]")
            return
            
        rec = self.recommendation_manager.recommend_best_product(products)
        if not rec:
            return
            
        best = rec["recommended"]
        p = best["product"]
        score_info = best["score_details"]
        
        console.print(Panel(
            f"[bold cyan]Recommended Product:[/bold cyan]\n"
            f"{p['name']} ({p['product_id']})\n"
            f"Price: {format_currency(p['price'])}\n"
            f"Purchase Score: [bold green]{score_info['score']}/100[/bold green]\n\n"
            f"[bold]Reasons:[/bold]\n" + 
            "\n".join(score_info['reasons']),
            title="SMART RECOMMENDATION"
        ))

    def analytics_menu(self):
        print("\n--- ANALYTICS ---")
        stats = self.analytics_manager.get_overall_analytics()
        
        panel = Panel(
            f"Total Products: {stats['total_products']}\n"
            f"Total Purchases: {stats['total_purchases']}\n"
            f"Total Spent: {format_currency(stats['total_spent'])}\n"
            f"Average Purchase: {format_currency(stats['average_purchase'])}\n"
            f"Budget Usage: {stats['budget_usage']:.1f}%",
            title="SHOPSMART ANALYTICS"
        )
        console.print(panel)

    def reports_menu(self):
        options = [
            ("1. View Overall Report", "1"),
            ("2. Export Reports to text file", "2"),
            ("3. Back", "3")
        ]
        c = interactive_menu("--- REPORTS ---", options)
        console.clear()
        
        if c == "1":
            print(self.report_manager.generate_overall_report())
        elif c == "2":
            filename = interactive_input("Enter filename (e.g., report.txt):")
            success, msg = self.report_manager.export_report_to_file(filename)
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")

    def backup_restore_menu(self):
        options = [
            ("1. Create Backup", "1"),
            ("2. Restore Backup", "2"),
            ("3. Back", "3")
        ]
        c = interactive_menu("--- BACKUP & RESTORE ---", options)
        console.clear()
        
        if c == "1":
            b = create_backup()
            if b:
                console.print(f"[green]Backup completed successfully.\nBackup folder: {b}[/green]")
            else:
                console.print("[red]Backup failed.[/red]")
        elif c == "2":
            backups = list_backups()
            if not backups:
                console.print("[yellow]No backups found.[/yellow]")
                return
            
            # Interactive backup selection
            backup_options = [(f"{idx}. {b}", b) for idx, b in enumerate(backups, 1)]
            backup_options.append(("Cancel", "cancel"))
            
            sel = interactive_menu("Select backup to restore:", backup_options)
            
            if sel != "cancel":
                success = restore_backup(sel)
                if success:
                    # reload data in managers
                    self.__init__()
                    console.print("[green]Backup restored successfully.[/green]")
                else:
                    console.print("[red]Restore failed.[/red]")

if __name__ == "__main__":
    app = ShopSmartApp()
    app.run()
