from typing import Dict, Any, List
from modules.analytics import AnalyticsManager
from utils.helpers import format_currency

class ReportManager:
    def __init__(self, analytics_manager: AnalyticsManager):
        self.analytics_manager = analytics_manager

    def generate_overall_report(self) -> str:
        stats = self.analytics_manager.get_overall_analytics()
        report = [
            "--- OVERALL SPENDING REPORT ---",
            f"Total Products:       {stats['total_products']}",
            f"Total Purchases:      {stats['total_purchases']}",
            f"Items Purchased:      {stats['total_items_purchased']}",
            f"Total Spent:          {format_currency(stats['total_spent'])}",
            f"Average Purchase:     {format_currency(stats['average_purchase'])}",
            f"Highest Purchase:     {format_currency(stats['highest_purchase'])}",
            f"Budget:               {format_currency(stats['budget'])}",
            f"Remaining:            {format_currency(stats['remaining_budget'])}",
            f"Budget Usage:         {stats['budget_usage']:.1f}%",
            "-------------------------------"
        ]
        return "\n".join(report)

    def generate_category_report(self) -> str:
        cat_stats = self.analytics_manager.get_category_spending()
        report = ["--- CATEGORY REPORT ---"]
        for cat, total in cat_stats["totals"].items():
            pct = cat_stats["percentages"][cat]
            report.append(f"{cat:20} {format_currency(total):15} ({pct:.1f}%)")
        report.append("-----------------------")
        highest = cat_stats["highest_category"]
        report.append(f"Highest Spending: {highest[0]} ({format_currency(highest[1])})")
        return "\n".join(report)

    def generate_store_report(self) -> str:
        store_stats = self.analytics_manager.get_store_spending()
        report = ["--- STORE REPORT ---"]
        for store, total in store_stats["totals"].items():
            count = store_stats["counts"][store]
            avg = store_stats["averages"][store]
            report.append(f"{store:20} {format_currency(total):15} | {count} purchases | {format_currency(avg)} avg")
        report.append("--------------------")
        highest = store_stats["highest_store"]
        report.append(f"Highest Spending Store: {highest[0]} ({format_currency(highest[1])})")
        return "\n".join(report)
        
    def generate_budget_report(self) -> str:
        stats = self.analytics_manager.get_overall_analytics()
        report = [
            "--- BUDGET REPORT ---",
            f"Allocated Budget: {format_currency(stats['budget'])}",
            f"Total Spent:      {format_currency(stats['total_spent'])}",
            f"Remaining:        {format_currency(stats['remaining_budget'])}",
            f"Utilization:      {stats['budget_usage']:.1f}%",
            "---------------------"
        ]
        return "\n".join(report)

    def export_report_to_file(self, filename: str) -> tuple[bool, str]:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.generate_overall_report() + "\n\n")
                f.write(self.generate_category_report() + "\n\n")
                f.write(self.generate_store_report() + "\n\n")
                f.write(self.generate_budget_report() + "\n")
            return True, f"Report exported successfully to {filename}"
        except Exception as e:
            return False, f"Failed to export report: {str(e)}"
