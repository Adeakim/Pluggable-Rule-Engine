from django.urls import path
from orders import views

urlpatterns = [
    path('check/', views.check_rules, name='check_rules'),
]

