from django.urls import path
from orders.views import CheckRulesView

urlpatterns = [
    path('check/', CheckRulesView.as_view(), name='check_rules'),
]

