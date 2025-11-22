"""
Simple pluggable rule engine with auto-registration.
Rules automatically register themselves when defined.
"""


class RuleRegistry:
    """Central registry for all rules."""
    _rules = {}

    @classmethod
    def register(cls, name, rule_class):
        """Register a rule by name."""
        cls._rules[name] = rule_class

    @classmethod
    def get_rule(cls, name):
        """Get a rule class by name."""
        return cls._rules.get(name)

    @classmethod
    def get_all_rules(cls):
        """Get all registered rules."""
        return cls._rules


class RuleMeta(type):
    """Metaclass that auto-registers rules."""
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Only register if it has a rule_name and is not the base class
        if 'rule_name' in attrs and attrs['rule_name']:
            RuleRegistry.register(attrs['rule_name'], cls)
        return cls


class BaseRule(metaclass=RuleMeta):
    """
    Base class for all rules.
    Subclasses must:
    - Define a rule_name class attribute
    - Implement the check() method
    """
    rule_name = None

    def check(self, order):
        """
        Check if the order passes this rule.
        Args:
            order: Order instance
        Returns:
            bool: True if rule passes, False otherwise
        """
        raise NotImplementedError("Subclasses must implement check()")

