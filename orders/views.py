from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from orders.rule_engine import RuleRegistry


@api_view(['POST'])
def check_rules(request):
    """
    Check which rules pass for a given order.
    
    Request body:
    {
        "order_id": 1,
        "rules": ["min_total_100", "min_items_2"]
    }
    
    Response:
    {
        "passed": true,
        "details": {
            "min_total_100": true,
            "min_items_2": false
        }
    }
    """
    order_id = request.data.get('order_id')
    rule_names = request.data.get('rules', [])

    # Validate input
    if not order_id:
        return Response(
            {"error": "order_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not rule_names:
        return Response(
            {"error": "rules list is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get the order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"error": f"Order with id {order_id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check each rule
    details = {}
    for rule_name in rule_names:
        rule_class = RuleRegistry.get_rule(rule_name)
        if not rule_class:
            details[rule_name] = None  # Rule not found
        else:
            rule_instance = rule_class()
            details[rule_name] = rule_instance.check(order)

    # Overall pass is True if all rules passed
    all_passed = all(
        result is True 
        for result in details.values()
    )

    return Response({
        "passed": all_passed,
        "details": details
    })

