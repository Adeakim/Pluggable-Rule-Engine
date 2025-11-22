from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from orders.models import Order
from orders.rule_engine import RuleRegistry
from orders.serializers import RuleCheckRequestSerializer, RuleCheckResponseSerializer


@extend_schema(
    request=RuleCheckRequestSerializer,
    responses=RuleCheckResponseSerializer,
    tags=['Rules'],
    examples=[
        OpenApiExample(
            'Example',
            value={'order_id': 1, 'rules': ['min_total_100', 'min_items_2']},
            request_only=True
        )
    ]
)
class CheckRulesView(APIView):
    """Check order against business rules."""

    def post(self, request):
        """Check which rules pass for a given order."""
        serializer = RuleCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_id = serializer.validated_data['order_id']
        rule_names = serializer.validated_data['rules']

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
                details[rule_name] = None
            else:
                rule_instance = rule_class()
                details[rule_name] = rule_instance.check(order)

        all_passed = all(result is True for result in details.values())

        return Response({
            "passed": all_passed,
            "details": details
        })