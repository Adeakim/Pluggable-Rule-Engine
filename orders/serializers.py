from rest_framework import serializers
from orders.rule_engine import RuleRegistry 

class RuleCheckRequestSerializer(serializers.Serializer):
    """Request serializer for rule checking."""
    order_id = serializers.IntegerField()
    rules = serializers.ListField(
        child=serializers.ChoiceField(
            choices=list(RuleRegistry.get_all_rules().keys()),
            help_text="Rule name: 'min_total_100', 'min_items_2', or 'divisible_by_5'"
        )
    )



class RuleCheckResponseSerializer(serializers.Serializer):
    """Response serializer for rule checking."""
    passed = serializers.BooleanField()
    details = serializers.DictField()
