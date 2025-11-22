"""
Rule implementations.
Each rule automatically registers itself via the BaseRule metaclass.
"""
from orders.rule_engine import BaseRule


class MinTotalRule(BaseRule):
    """Check if order total is greater than 100."""
    rule_name = "min_total_100"

    def check(self, order):
        return order.total > 100


class MinItemsRule(BaseRule):
    """Check if order has at least 2 items."""
    rule_name = "min_items_2"

    def check(self, order):
        return order.items_count >= 2


class DivisibleByFiveRule(BaseRule):
    """Check if order total is divisible by 5."""
    rule_name = "divisible_by_5"

    def check(self, order):
        return order.total % 5 == 0

