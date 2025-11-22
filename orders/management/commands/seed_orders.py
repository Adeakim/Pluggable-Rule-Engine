from django.core.management.base import BaseCommand
from orders.models import Order


class Command(BaseCommand):
    help = 'Seed the database with 3 example orders'

    def handle(self, *args, **options):
        # Clear existing orders
        Order.objects.all().delete()

        # Create 3 example orders
        orders = [
            Order(total=150.00, items_count=3),  # Passes: total>100, items>=2, divisible by 5
            Order(total=75.50, items_count=1),   # Fails all rules
            Order(total=95.00, items_count=2),   # Passes: items>=2, divisible by 5
        ]

        Order.objects.bulk_create(orders)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(orders)} orders:'))
        for order in Order.objects.all():
            self.stdout.write(f'  - Order {order.id}: ${order.total}, {order.items_count} items')

